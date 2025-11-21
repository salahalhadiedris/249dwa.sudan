from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list_view, name='category_list'),
]