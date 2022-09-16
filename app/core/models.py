"""
Model definitions.
"""
from django.db import models


class Recipe(models.Model):
    """Model definition for a recipe."""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name
