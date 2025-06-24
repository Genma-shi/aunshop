from django.db import models
from books.models import Book
from stationery.models import Stationery
from promotions.models import Promotion

class CartItem(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    stationery = models.ForeignKey(Stationery, on_delete=models.CASCADE, null=True, blank=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        item = self.book or self.stationery or self.promotion
        return f"{item} x {self.quantity}"