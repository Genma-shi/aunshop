from django.contrib.auth import authenticate
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser

class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        fields = ['phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone_number'] = user.phone_number
        token['full_name'] = f"{user.first_name} {user.last_name}"
        return token

    def validate(self, attrs):
        try:
            if self.context['request'].body:
                self.context['request'].body.decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            raise serializers.ValidationError({"error": "Invalid encoding in request body"})
        try:
            user = CustomUser.objects.get(phone_number=attrs['phone_number'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"detail": "No active account found with the given credentials"})
        credentials = {
            'username': attrs['phone_number'],
            'password': attrs['password']
        }
        return super().validate(credentials)

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        if CustomUser.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "Phone number already exists"})
        if attrs.get('email') and CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2', None)
        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user

class NotificationSettingSerializer(serializers.Serializer):
    notifications_enabled = serializers.BooleanField()

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'email']

class FCMTokenSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=255)
