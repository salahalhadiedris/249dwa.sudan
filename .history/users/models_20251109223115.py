from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    city = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_pharmacist = models.BooleanField(default=False)

    def __str__(self):
        return self.username
