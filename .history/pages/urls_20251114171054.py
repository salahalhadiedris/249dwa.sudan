from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('detalise/', views.detalise, name='detalise'),
    path('product/<int:pk>/', views.detalise, name='detalise'), 
    path('pharmacies/', views.pharmacies, name='pharmacies'),
    path('cosmo/', views.cosmo, name='cosmo'),
]