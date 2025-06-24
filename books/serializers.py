from rest_framework import serializers
from .models import Book, Subject

class BookSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    class Meta:
        model = Book
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'