from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('products/', views.products, name='products'),
    path('pharmacies/', views.pharmacies, name='pharmacies'),
    path('cosmo/', views.cosmo, name='cosmo'),
]