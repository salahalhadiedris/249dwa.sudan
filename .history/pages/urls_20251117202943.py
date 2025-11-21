from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/categories/', views.get_categories, name='get_categories'),
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('pharmacies/', views.pharmacies, name='pharmacies'),
    path('cosmo/', views.cosmo, name='cosmo'),
    path('search/', views.search_products, name='search_products'),
]