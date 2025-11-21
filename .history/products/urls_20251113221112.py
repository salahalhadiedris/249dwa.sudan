from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name='products'),
    path('api/pharmacies/', views.get_pharmacies_for_product, name='api-pharmacies'),
    # يمكن إضافة المزيد من المسارات هنا
]
