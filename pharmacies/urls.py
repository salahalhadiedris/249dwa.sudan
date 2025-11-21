from django.urls import path
from . import views

urlpatterns = [
    path('', views.pharmacies, name='pharmacies'),
]