from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Variation(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип вариации")
    value = models.CharField(max_length=100, verbose_name="Значение вариации")
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Изменение цены")

    class Meta:
        verbose_name = "Вариация"
        verbose_name_plural = "Вариации"

    def __str__(self):
        return f"{self.name}: {self.value}"

class Stationery(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    images = models.ManyToManyField('StationeryImage', verbose_name="Изображения")
    brand = models.CharField(max_length=100, verbose_name="Бренд")
    description = models.TextField(verbose_name="Описание")
    variations = models.ManyToManyField(Variation, verbose_name="Вариации")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Канцелярский товар"
        verbose_name_plural = "Канцелярские товары"

    def __str__(self):
        return self.title

class StationeryImage(models.Model):
    image = models.ImageField(upload_to='stationery/', verbose_name="Изображение")

    class Meta:
        verbose_name = "Изображение канцелярии"
        verbose_name_plural = "Изображения канцелярии"

    def __str__(self):
        return str(self.image)