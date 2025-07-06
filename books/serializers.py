from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'image', 'book_class', 'author', 'language', 'subject', 'price', 'description', 'created_at']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
