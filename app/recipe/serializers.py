"""
Recipe API serializers.
"""
from rest_framework import serializers

from core.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the ingredient model."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the recipe model."""
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients']
        read_only_fields = ['id']

    def _add_ingredients(self, ingredients, recipe):
        """Get or create ingredients."""
        for ingredient in ingredients:
            ingredient_obj, _ = Ingredient.objects.get_or_create(**ingredient)
            recipe.ingredients.add(ingredient_obj)

    def create(self, data):
        """Create a recipe."""
        ingredients = data.pop('ingredients', [])
        recipe = Recipe.objects.create(**data)
        self._add_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, data):
        """Update a recipe."""
        ingredients = data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, val in data.items():
            setattr(instance, attr, val)

        instance.save()
        return instance
