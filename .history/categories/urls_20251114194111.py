from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('categories/', views.category_list, name='category_list'),
    path('products/', views.product_list, name='product_list'),
    path('products/category/<slug:category_slug>/', views.product_list, name='products_by_category'),
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('filter-products/', views.filter_products_ajax, name='filter_products_ajax'),
]