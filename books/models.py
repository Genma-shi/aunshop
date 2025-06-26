from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class Book(models.Model):
    LANGUAGE_CHOICES = [
        ('KG', 'Кыргызский'),
        ('RU', 'Русский'),
        ('EN', 'Английский'),
    ]
    CLASS_CHOICES = [
        ('preschool', 'Дошкольный'),
        ('1', '1 класс'),
        ('2', '2 класс'),
        ('3', '3 класс'),
        ('4', '4 класс'),
        ('5', '5 класс'),
        ('6', '6 класс'),
        ('7', '7 класс'),
        ('8', '8 класс'),
        ('9', '9 класс'),
        ('10', '10 класс'),
        ('11', '11 класс'),
    ]
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    author = models.CharField(max_length=100)
    book_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    image = models.ImageField(upload_to='books/')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title