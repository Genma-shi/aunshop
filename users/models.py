from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия"
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="Номер телефона"
    )
    email = models.EmailField(
        unique=True,
        blank=True,  # ← Сделали необязательным
        null=True,   # ← Сделали необязательным
        verbose_name="Электронная почта"
    )
    fcm_token = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="FCM-токен"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
