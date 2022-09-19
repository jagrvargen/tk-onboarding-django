"""
Contains tests for the recipe API.
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def create_recipe(name):
    """Create a sample recipe."""
    return Recipe.objects.create(name=name)


class RecipeAPITests(TestCase):
    """Tests the recipe API."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """Test retrieve all recipes."""
        create_recipe('Salad')
        create_recipe('Sauce')

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipe_by_name(self):
        """Test retrieve specific recipe by name."""
        create_recipe('Sausage')
        create_recipe('Sandwich')

        res = self.client.get(RECIPES_URL, {'name': 'Sausage'})
        recipe = Recipe.objects.filter(name='Sausage')
        serializer = RecipeSerializer(recipe, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertNotIn('Sandwich', res.data)

    def test_create_recipe(self):
        """Test create a recipe with POST request."""
        pass