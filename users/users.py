from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Кастомный менеджер пользователя
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('Email или номер телефона должны быть указаны')
        email = self.normalize_email(email) if email else None
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь is_superuser=True.')

        return self.create_user(email, phone_number, password, **extra_fields)


# Кастомная модель пользователя без поля username
class CustomUser(AbstractUser):
    username = None  # Отключаем поле username

    first_name = models.CharField(max_length=50, verbose_name=_("Имя"))
    last_name = models.CharField(max_length=50, verbose_name=_("Фамилия"))
    phone_number = models.CharField(max_length=15, unique=True, verbose_name=_("Номер телефона"))
    email = models.EmailField(unique=True, verbose_name=_("Электронная почта"))
    fcm_token = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("FCM-токен"))

    USERNAME_FIELD = 'email'  # Логин по email
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# Сериализатор для регистрации пользователя
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        # заменим username на phone_number
        self.user = self.context['request'].user  # тут неверно!
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


# Представление регистрации
from rest_framework import generics
from .models import CustomUser

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []  # Можно AllowAny если надо
