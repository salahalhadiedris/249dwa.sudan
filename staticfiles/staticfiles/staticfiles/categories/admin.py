from django.contrib import admin
from .models import Category

# admin.py

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color', 'views', 'is_active']
    list_editable = ['icon', 'color', 'views']
    prepopulated_fields = {'slug': ('name',)}