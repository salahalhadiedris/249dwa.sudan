from django.shortcuts import render
from .models import Product
from categories.models import Category

def product_list(request):
    category_id = request.GET.get('category')
    city = request.GET.get('city')

    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)
    if city:
        products = products.filter(city__iexact=city)

    categories = Category.objects.all()
    cities = Product.objects.values_list('city', flat=True).distinct()

    context = {
        'products': products,
        'categories': categories,
        'cities': cities,
    }
    return render(request, 'products/product_list.html', context)
