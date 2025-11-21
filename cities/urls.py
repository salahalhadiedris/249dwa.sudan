from django.urls import path
from . import views

urlpatterns = [
    path('cities_list/', views.cities_list, name='cities_list'),
]