from django.contrib import admin

from main.models import Driver

# Register your models here.

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rating')
    list_filter = ('category',)
    search_fields = ('name',)
