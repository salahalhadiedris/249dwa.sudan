from django.urls import path
from . import views

urlpatterns = [
    path('product_list/', views.drugs_list_view, name='product_list'),
    path('api/pharmacies/', views.get_pharmacies_for_product, name='api-pharmacies'),
    path('search/', views.search_products, name='search_products'),

    # يمكن إضافة المزيد من المسارات هنا
]
