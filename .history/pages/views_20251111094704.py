from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product
# Create your views here.


def home(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'pages/products.html',)

def about(request):
    return render(request, 'pages/about.html')

def pharmacies(request):
    return render(request, 'pages/pharmacies.html')

def cosmo(request):
    return render(request, 'pages/cosmo.html')