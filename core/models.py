# core/models.py
from django.db import models

class PageContent(models.Model):
    KEY_CHOICES = [
        ('about_us', 'О нас'),
        ('branches', 'Наши филиалы'),
        ('privacy_policy', 'Политика конфиденциальности'),
    ]
    key = models.CharField(max_length=50, choices=KEY_CHOICES, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    class Meta:
        verbose_name = 'Карточка информаций'
        verbose_name_plural = 'Карточки информация'
    
    def __str__(self):
        return self.get_key_display()
