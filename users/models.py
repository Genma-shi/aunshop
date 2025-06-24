from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self): return f"{self.first_name} {self.last_name}"