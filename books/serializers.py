from rest_framework import serializers
from .models import Book, Subject

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'image' , 'book_class' , 'author' , 'language', 'subject', 'price', 'description', 'created_at']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

