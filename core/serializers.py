# core/serializers.py
from rest_framework import serializers
from .models import PageContent , ContactPhoneNumber

class PageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageContent
        fields = ['key', 'title', 'description']

class ContactPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPhoneNumber
        fields = ['phone_number']