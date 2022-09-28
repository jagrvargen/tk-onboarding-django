"""
Ingredients API tests.
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    """Create and return an ingredient detail URL."""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


class IngredientsAPITests(TestCase):
    """Test ingredients API."""

    def setUp(self):
        self.client = APIClient()

    def test_list_ingredients(self):
        Ingredient.objects.create(name='Salt')
        Ingredient.objects.create(name='Water')

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['name'], ingredients.values()[0]['name'])
        self.assertEqual(res.data[1]['name'], ingredients.values()[1]['name'])
        self.assertEqual(res.data[0]['id'], ingredients.values()[0]['id'])
        self.assertEqual(res.data[1]['id'], ingredients.values()[1]['id'])

    def test_update_ingredient(self):
        """Test updating an ingredient"""
        ingredient = Ingredient.objects.create(name='Pepper')

        payload = {'name': 'Salt'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        ingredient1 = Ingredient.objects.create(name='Mayonnaise')
        Ingredient.objects.create(name='Aioli')

        url = detail_url(ingredient1.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.all()
        self.assertEqual(ingredients.filter(name='Mayonnaise').count(), 0)
        self.assertIsNotNone(ingredients.get(name='Aioli'))
