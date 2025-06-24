from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class Variation(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self): return f"{self.name}: {self.value}"

class Stationery(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ManyToManyField('StationeryImage')
    brand = models.CharField(max_length=100)
    description = models.TextField()
    variations = models.ManyToManyField(Variation)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class StationeryImage(models.Model):
    image = models.ImageField(upload_to='stationery/')
    def __str__(self): return str(self.image)