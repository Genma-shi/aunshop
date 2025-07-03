from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        attrs['username'] = attrs.get('phone_number')
        return super().validate(attrs)


    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2', None)
        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user 


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'email']

class FCMTokenSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=255)