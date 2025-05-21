from django.db import models

from .constants import RATING_CHOICES, CATEGORY_CHOICES


# Create your models here.

class Driver(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    class Meta:
        ordering = ['category', 'name']
