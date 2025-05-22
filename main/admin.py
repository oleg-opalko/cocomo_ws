from django.contrib import admin

from main.models import Driver
from .models import Project, ScaleDriver, CostDriver, ProjectScaleDriver, ProjectCostDriver

# Register your models here.

# @admin.register(Driver)
# class DriverAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'rating')
#     list_filter = ('category',)
#     search_fields = ('name',)

@admin.register(ScaleDriver)
class ScaleDriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'weight')
    search_fields = ('name',)

@admin.register(CostDriver)
class CostDriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'rating', 'category', 'effort_multiplier')
    list_filter = ('rating', 'category')
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_family', 'size_kloc')
    list_filter = ('model_family',)

@admin.register(ProjectScaleDriver)
class ProjectScaleDriverAdmin(admin.ModelAdmin):
    list_display = ('project', 'scale_driver', 'rating')
    list_filter = ('rating',)

@admin.register(ProjectCostDriver)
class ProjectCostDriverAdmin(admin.ModelAdmin):
    list_display = ('project', 'cost_driver', 'rating')
    list_filter = ('rating',)
