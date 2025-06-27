from rest_framework import serializers
from .models import Stationery, Category, Variation, StationeryImage

class StationeryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationeryImage
        fields = ['image']

class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ['name', 'value', 'price_modifier']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class StationerySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Stationery
        fields = ['id', 'title', 'category', 'category_id', 'price', 'description', 'created_at']

