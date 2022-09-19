"""
Model definitions.
"""
from django.db import models


class Recipe(models.Model):
    """Model definition for a recipe."""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024, null=True, blank=True)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Model definition for an ingredient"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
