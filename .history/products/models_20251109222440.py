from django.db import models
from pharmacies.models import Pharmacy

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
