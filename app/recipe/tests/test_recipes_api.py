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


def create_ingredient(name):
    """Create a sample ingredient."""
    return Ingredient.objects.create(name=name)


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

    def test_create_recipe_with_ingredient(self):
        """Test create a recipe with an ingredient."""
        payload = {
            'name': 'Delicious Soup',
            'description': 'Hot Soup',
            'ingredients': [{'name': 'Salt'}, {'name': 'Water'}]
        }
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        print(f"RES CONTAINS {res.data}")

    # def test_create_recipe_with_ingredients(self):
    #     """Test create a recipe with ingredients."""
    #     payload = {
    #         'name': 'Soup',
    #         'description': 'A most delicious soup',
    #         'ingredients': [{'name': 'Water'}, {'name': 'Salt'}],
    #     }
    #     res = self.client.post(RECIPES_URL, payload)
    #     check = self.client.get(INGREDIENTS_URL)
    #     print(f"CHECK INGREDIENTS {check.data}")
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     print(f"RES CONTAINS ~~~~> {res.data}")
    #     self.assertIn('Water', res.data['ingredients'].values())
