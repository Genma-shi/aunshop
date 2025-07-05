from rest_framework import serializers
from .models import Promotion, PromotionImage

class PromotionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionImage
        fields = ['image']

class PromotionSerializer(serializers.ModelSerializer):
    images = PromotionImageSerializer(many=True)
    class Meta:
        model = Promotion
        fields = '__all__'