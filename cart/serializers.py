from rest_framework import serializers
from .models import CartItem
from books.serializers import BookSerializer
from stationery.serializers import StationerySerializer
from promotions.serializers import PromotionSerializer

class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    stationery = StationerySerializer(read_only=True)
    promotion = PromotionSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'book', 'stationery', 'promotion', 'quantity']