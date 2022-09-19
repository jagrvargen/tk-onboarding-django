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


class IngredientsAPITests(TestCase):
    """Test ingredients API."""

    def setUp(self):
        self.client = APIClient()

    def test_get_ingredients(self):
        Ingredient.objects.create(name='Salt')
        Ingredient.objects.create(name='Water')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
