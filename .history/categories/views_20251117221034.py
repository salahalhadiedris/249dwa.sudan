# views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category

def product_list(request, category_slug=None):
    """عرض المنتجات مع إمكانية الفلترة حسب الفئة"""
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(in_stock=True)
  