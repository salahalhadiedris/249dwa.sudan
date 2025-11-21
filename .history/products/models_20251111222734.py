from django.db import models
from categories.models import Category
from pharmacies.models import Pharmacy

class Product(models.Model):
    
    name = models.CharField(max_length=300, verbose_name="اسم الدواء (عربي)")
    name_english = models.CharField(max_length=300, blank=True, null=True, verbose_name="اسم الدواء (إنجليزي)")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    strength = models.CharField(max_length=100, blank=True, null=True, verbose_name="التركيز")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="السعر")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="الفئة")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="المدينة")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="صورة الدواء")
    pharmacies = models.ManyToManyField(Pharmacy, blank=True, related_name='products', verbose_name="الصيدليات المتوفرة")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    views = models.IntegerField(default=0, verbose_name="عدد المشاهدات")
    clicks = models.IntegerField(default=0, verbose_name="عدد النقرات")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_available_pharmacies(self, city=None):
        """جلب الصيدليات المتوفرة لهذا المنتج"""
        pharmacies = self.pharmacies.filter(is_active=True)
        if city:
            pharmacies = pharmacies.filter(city=city)
        return pharmacies