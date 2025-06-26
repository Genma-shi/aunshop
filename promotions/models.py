from django.db import models

class Promotion(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название акции"
    )
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Старая цена"
    )
    new_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Новая цена"
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    images = models.ManyToManyField(
        'PromotionImage',
        verbose_name="Изображения"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def __str__(self):
        return self.title


class PromotionImage(models.Model):
    image = models.ImageField(
        upload_to='promotions/',
        verbose_name="Изображение"
    )

    class Meta:
        verbose_name = "Изображение акции"
        verbose_name_plural = "Изображения акций"

    def __str__(self):
        return str(self.image)
