from rest_framework import serializers
from .models import Stationery, Category, Variation, StationeryImage
from drf_spectacular.utils import extend_schema_field

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

class StationeryListSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Stationery
        fields = ['id', 'title', 'price', 'description', 'first_image']
    
    @extend_schema_field(str)
    def get_first_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            request = self.context.get('request')
            return request.build_absolute_uri(first_image.image.url) if request else first_image.image.url
        return None

class StationerySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    images = StationeryImageSerializer(many=True, read_only=True)
    variations = VariationSerializer(many=True, read_only=True)
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Stationery
        fields = [
            'id', 'title', 'category', 'category_id', 'price', 'brand',
            'description', 'images', 'variations', 'first_image', 'created_at'
        ]

    @extend_schema_field(str)
    def get_first_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            request = self.context.get('request')
            return request.build_absolute_uri(first_image.image.url) if request else first_image.image.url
        return None
