from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),          # الصفحة الرئيسية
    path('about/', views.about, name='about'),  # صفحة من نحن
    path('contact/', views.contact, name='contact'),  # صفحة التواصل
]
