from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Êàñòîìíûé ìåíåäæåð ïîëüçîâàòåëÿ
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number must be provided')
        email = self.normalize_email(email) if email else None
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, email, password, **extra_fields)

# Êàñòîìíàÿ ìîäåëü ïîëüçîâàòåëÿ
class CustomUser(AbstractUser):
    username = None  # Îòêëþ÷åíèå ïîëÿ username
    first_name = models.CharField(max_length=50, verbose_name=_("First name"), blank=False)
    last_name = models.CharField(max_length=50, verbose_name=_("Last name"), blank=False)
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        verbose_name=_("Phone number"),
        blank=False,
        help_text=_("Enter phone number in international format, e.g. +1234567890")
    )
    email = models.EmailField(unique=True, verbose_name=_("Email address"), blank=True, null=True)
    fcm_token = models.CharField(max_length=255, verbose_name=_("FCM token"), blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email or 'no email'})"

# Ñåðèàëèçàòîð äëÿ ïîëó÷åíèÿ JWT-òîêåíà ïî íîìåðó òåëåôîíà
class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
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
            user = CustomUser.objects.get(phone_number=attrs['phone_number'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"detail": "No active account found with the given credentials"})
        credentials = {
            'username': attrs['phone_number'],  # Äëÿ ñîâìåñòèìîñòè ñ backend
            'password': attrs['password']
        }
        return super().validate(credentials)

# Ñåðèàëèçàòîð äëÿ ðåãèñòðàöèè
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
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2', None)
        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user

# Ñåðèàëèçàòîð äëÿ ëîãèíà
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

# Ñåðèàëèçàòîð äëÿ ïðîôèëÿ ïîëüçîâàòåëÿ
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'email']

# Ñåðèàëèçàòîð äëÿ FCM-òîêåíà
class FCMTokenSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=255)