from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
import math

from .constants import RATING_CHOICES, CATEGORY_CHOICES, MODEL_FAMILIES


# Create your models here.

class Driver(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['category', 'name']

class ScaleDriver(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    weight = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Weight factor for the scale driver (0.0 to 1.0)"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class CostDriver(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    effort_multiplier = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Effort multiplier for this cost driver"
    )

    def __str__(self):
        return f"{self.name} ({self.get_rating_display()})"

    class Meta:
        ordering = ['category', 'name']

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    model_family = models.CharField(max_length=20, choices=MODEL_FAMILIES)
    size_kloc = models.PositiveIntegerField(
        validators=[MinValueValidator(0.0)],
        help_text="Size in thousands of lines of code (KLOC)"
    )
    scale_drivers = models.ManyToManyField(ScaleDriver, through='ProjectScaleDriver')
    cost_drivers = models.ManyToManyField(CostDriver, through='ProjectCostDriver')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_model_family_display()})"

    class Meta:
        ordering = ['-created_at']

    def calculate_scale_factor(self):
        """Calculate the scale factor (B) based on scale drivers"""
        scale_factor = 0
        for project_scale in self.projectscaledriver_set.all():
            scale_factor += project_scale.scale_driver.weight * (project_scale.rating - 3)
        return scale_factor

    def calculate_effort_adjustment_factor(self):
        """Calculate the Effort Adjustment Factor (EAF) based on cost drivers"""
        eaf = 1.0
        for project_cost in self.projectcostdriver_set.all():
            eaf *= project_cost.cost_driver.effort_multiplier
        return eaf

    def calculate_effort(self):
        """Calculate the effort in person-months using COCOMO II equation"""
        b = self.calculate_scale_factor()
        eaf = self.calculate_effort_adjustment_factor()
        a = 2.94  # COCOMO II constant
        
        effort = a * eaf * math.pow(self.size_kloc, b)
        return round(effort, 2)

    def calculate_schedule(self):
        """Calculate the schedule in months using COCOMO II equation"""
        effort = self.calculate_effort()
        b = self.calculate_scale_factor()
        c = 3.67  # COCOMO II constant
        d = 0.28  # COCOMO II constant
        
        schedule = c * math.pow(effort, d)
        return round(schedule, 2)

    def calculate_staffing(self):
        """Calculate the average staffing level"""
        effort = self.calculate_effort()
        schedule = self.calculate_schedule()
        return round(effort / schedule, 2)

    def get_calculation_results(self):
        """Get all calculation results in a dictionary"""
        return {
            'effort': self.calculate_effort(),
            'schedule': self.calculate_schedule(),
            'staffing': self.calculate_staffing(),
            'scale_factor': self.calculate_scale_factor(),
            'eaf': self.calculate_effort_adjustment_factor()
        }

class ProjectScaleDriver(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    scale_driver = models.ForeignKey(ScaleDriver, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)

    class Meta:
        unique_together = ['project', 'scale_driver']

class ProjectCostDriver(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    cost_driver = models.ForeignKey(CostDriver, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)

    class Meta:
        unique_together = ['project', 'cost_driver']
