"""
Tests for custom models.
"""
from django.test import TestCase

from core.models import Recipe, Ingredient


class ModelTests(TestCase):
    """Tests for the recipe model."""

    def test_create_recipe(self):
        """Test creating a recipe."""
        name = 'Foie Gras'
        recipe = Recipe.objects.create(name=name)

        self.assertEqual(recipe.name, name)
        self.assertEqual(str(recipe), name)

    def test_create_ingredient(self):
        """Test creating an ingredient."""
        recipe_name = 'Foie Gras'
        recipe = Recipe.objects.create(name=recipe_name)

        ingredient_name = 'Salt'
        ingredient = Ingredient.objects.create(name=ingredient_name, recipe=recipe)

        self.assertEqual(ingredient.name, ingredient_name)
        self.assertEqual(str(ingredient), ingredient_name)
