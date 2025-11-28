from django.shortcuts import render
from .models import Product
from pharmacies.models import Pharmacy

def product_list(request):
    category_id = request.GET.get('category')
    city = request.GET.get('city')


