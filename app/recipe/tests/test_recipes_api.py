"""
Contains tests for the recipe API.
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def create_recipe(**params):
    """Create a sample recipe."""
    defaults = {
        'name': 'Test recipe name',
        'description': 'Test recipe description',
    }
    defaults.update(params)
    return Recipe.objects.create(**defaults)


def detail_url(recipe_id):
    """Create and return a recipe detail URL."""
    return reverse('recipe:recipe-detail', args=[recipe_id])


class RecipeAPITests(TestCase):
    """Tests the recipe API."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """Test retrieve all recipes."""
        recipe1 = {'name': 'Salad'}
        recipe2 = {'name': 'Sauce'}
        create_recipe(**recipe1)
        create_recipe(**recipe2)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipe_by_name(self):
        """Test retrieve specific recipe by name."""
        recipe1 = {'name': 'Sausage'}
        recipe2 = {'name': 'Sandwich'}
        create_recipe(**recipe1)
        create_recipe(**recipe2)

        res = self.client.get(RECIPES_URL, {'name': 'Sausage'})
        recipe = Recipe.objects.filter(name='Sausage')
        serializer = RecipeSerializer(recipe, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertNotIn('Sandwich', res.data)

    def test_create_recipe(self):
        """Test create a recipe with POST request."""
        payload = {
            'name': 'Single Pancake',
            'description': 'Just one single pancake',
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

    def test_partial_update_recipe(self):
        """Test partial update of a recipe."""
        original_name = 'Bread'
        original_description = 'Flour and water'
        recipe = Recipe.objects.create(name=original_name,
                                       description=original_description)
        payload = {'name': 'Pan'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, original_description)

    def test_full_update_recipe(self):
        """Test full update of a recipe."""
        original_name = 'Bread'
        original_description = 'Flour and water'
        recipe = Recipe.objects.create(name=original_name,
                                       description=original_description)
        payload = {'name': 'Pan', 'description': 'Flour, water, and salt'}
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])

    def test_delete_recipe(self):
        """Test deleting a recipe successful."""
        recipe = create_recipe()

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_create_recipe_with_ingredients(self):
        """Test create a recipe with an ingredient."""
        payload = {
            'name': 'Delicious Soup',
            'description': 'Hot Soup',
            'ingredients': [{'name': 'Salt'}, {'name': 'Water'}]
        }
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual('Salt', res.data['ingredients'][0]['name'])
        self.assertEqual('Water', res.data['ingredients'][1]['name'])

    def test_create_recipe_with_existing_ingredient(self):
        """Test creating a recipe with existing ingredient."""
        ingredient = Ingredient.objects.create(name='Pepper')
        payload = {
            'name': 'Pepper Sandwich',
            'ingredients': [{'name': 'Pepper'}, {'name': 'Bread'}],
        }
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.all()
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertIn(ingredient, recipe.ingredients.all())
        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(name=ingredient['name']).exists()
            self.assertTrue(exists)