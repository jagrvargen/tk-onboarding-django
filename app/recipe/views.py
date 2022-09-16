"""
Recipe viewsets
"""
from rest_framework import viewsets

from core.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset for the recipe API."""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Fetch all recipes."""
        return self.queryset.order_by('-id')
