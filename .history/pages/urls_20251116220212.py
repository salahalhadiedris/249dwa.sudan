from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<int:product_id=product.id>/', views.product_detail, name='product_detail'),
    path('pharmacies/', views.pharmacies, name='pharmacies'),
    path('cosmo/', views.cosmo, name='cosmo'),
    path('search/', views.search_products, name='search_products'),
]