"""
Recipe API serializers.
"""
from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the recipe model."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)
