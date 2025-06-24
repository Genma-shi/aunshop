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

class StationerySerializer(serializers.ModelSerializer):
    images = StationeryImageSerializer(many=True)
    variations = VariationSerializer(many=True)
    category = serializers.StringRelatedField()
    class Meta:
        model = Stationery
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'