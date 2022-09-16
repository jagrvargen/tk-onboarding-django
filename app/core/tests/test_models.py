"""
Tests for custom models.
"""
from django.test import TestCase

from core.models import Recipe


class RecipeTests(TestCase):
    """Tests for the recipe model."""

    def test_create_recipe_successful(self):
        """Test a recipe is successfully created."""
        name = 'Foie Gras'
        recipe = Recipe.objects.create(name=name)

        self.assertEqual(recipe.name, name)
