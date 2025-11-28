from django.urls import path
from . import views

urlpatterns = [
    path('cities_list/', views.cities_list_view, name='cities_list'),
]