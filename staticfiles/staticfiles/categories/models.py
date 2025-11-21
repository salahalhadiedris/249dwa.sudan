from django.db import models

class Category(models.Model):
    """نموذج الفئات (تصنيفات الأدوية)"""
    name = models.CharField(max_length=200, verbose_name="اسم الفئة")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name="أيقونة")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "فئة"
        verbose_name_plural = "الفئات"
        ordering = ['name']
    
    def __str__(self):
        return self.name