from django.db import models

# models.py
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم الفئة")
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, verbose_name="الأيقونة")
    color = models.CharField(max_length=7, default="#3b82f6", verbose_name="اللون")
    views = models.IntegerField(default=0, verbose_name="عدد المشاهدات")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'فئة الأدوية'
        verbose_name_plural = 'فئات الأدوية'
    
    def __str__(self):
        return self.name