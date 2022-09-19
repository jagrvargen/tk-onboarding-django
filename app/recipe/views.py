"""
Recipe viewsets
"""
from rest_framework import viewsets, mixins

from core.models import Recipe, Ingredient
from recipe.serializers import RecipeSerializer, IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset for the recipe API."""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Fetch recipes."""
        name = self.request.query_params.get('name')
        if name:
            return self.queryset.filter(name=name)

        return self.queryset.order_by('-id')

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save()


class IngredientViewSet(mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """Viewset for the ingredient API."""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        """Fetch ingredients."""
        return self.queryset.order_by('-name')
