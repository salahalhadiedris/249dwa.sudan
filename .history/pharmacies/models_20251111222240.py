from django.db import models
from categories.models import Category
from pharmacies.models import Pharmacy

    """نموذج الصيدليات"""
    name = models.CharField(max_length=200, verbose_name="اسم الصيدلية")
    city = models.CharField(max_length=100, verbose_name="المدينة")
    location = models.CharField(max_length=300, blank=True, null=True, verbose_name="الموقع")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الهاتف")
    whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الواتساب")
    email = models.EmailField(blank=True, null=True, verbose_name="البريد الإلكتروني")
    image = models.ImageField(upload_to='pharmacies/', blank=True, null=True, verbose_name="صورة الصيدلية")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.5, verbose_name="التقييم")
    rating_count = models.IntegerField(default=0, verbose_name="عدد التقييمات")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    is_featured = models.BooleanField(default=False, verbose_name="مميز")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "صيدلية"
        verbose_name_plural = "الصيدليات"
        ordering = ['-is_featured', '-rating', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.city}"