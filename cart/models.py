from django.db import models
from books.models import Book
from stationery.models import Stationery
from promotions.models import Promotion

class CartItem(models.Model):
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Ключ сессии"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Книга"
    )
    stationery = models.ForeignKey(
        Stationery,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Канцелярский товар"
    )
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Акция"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def __str__(self):
        item = self.book or self.stationery or self.promotion
        return f"{item} — {self.quantity} шт."
