from django.urls import path
from . import views

urlpatterns = [
    path('', views.pharmacy_list, name='pharmacy_list'),
    path('<int:pharmacy_id>/', views.pharmacy_detail, name='pharmacy_detail'),
    path('create/', views.create_pharmacy, name='create_pharmacy'),
    path('<int:pharmacy_id>/edit/', views.edit_pharmacy, name='edit_pharmacy'),
    path('<int:pharmacy_id>/delete/', views.delete_pharmacy, name='delete_pharmacy'),
    path('<int:pharmacy_id>/products/', views.pharmacy_products, name='pharmacy_products'),
]