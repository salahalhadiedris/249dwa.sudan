from django.shortcuts import render
from products.models import Product

def home(request):
    Products = Product.objects.all()

    return render(request, 'pages/ home.html', {'products': Products})

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')