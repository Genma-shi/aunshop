from django.db import models

class Promotion(models.Model):
    title = models.CharField(max_length=200)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    images = models.ManyToManyField('PromotionImage')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class PromotionImage(models.Model):
    image = models.ImageField(upload_to='promotions/')
    def __str__(self): return str(self.image)