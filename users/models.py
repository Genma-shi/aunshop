from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('Email РёР»Рё РЅРѕРјРµСЂ С‚РµР»РµС„РѕРЅР° РґРѕР»Р¶РЅС‹ Р±С‹С‚СЊ СѓРєР°Р·Р°РЅС‹')
        email = self.normalize_email(email) if email else None
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True) 
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser РґРѕР»Р¶РµРЅ РёРјРµС‚СЊ is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser РґРѕР»Р¶РµРЅ РёРјРµС‚СЊ is_superuser=True.')
        return self.create_user(email, phone_number, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50, verbose_name=_("Имя"), blank=False)
    last_name = models.CharField(max_length=50, verbose_name=_("Фамилия"), blank=False)
    phone_number = models.CharField(
        max_length=15, unique=True,
        verbose_name=_("Номер телефона"),
        blank=False,
        help_text=_("Введите номер телефона в международном формате, например +996700333111")
    )
    email = models.EmailField(unique=True, verbose_name=_("Электронная почта"), blank=True , null=True)
    fcm_token = models.CharField(max_length=255, verbose_name=_("FCM-токен"), blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


    objects = CustomUserManager()

    class Meta:
        verbose_name = _("РџРѕР»СЊР·РѕРІР°С‚РµР»СЊ")
        verbose_name_plural = _("РџРѕР»СЊР·РѕРІР°С‚РµР»Рё")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"