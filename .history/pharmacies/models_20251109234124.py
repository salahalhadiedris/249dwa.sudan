from django.db import models

class Pharmacy(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.city}"
