from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/category/<slug:category_slug>/', views.Category, name='category_products'), 
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('pharmacies/', views.pharmacies, name='pharmacies'),
    path('cosmo/', views.cosmo, name='cosmo'),
    path('search/', views.search_products, name='search_products'),
]