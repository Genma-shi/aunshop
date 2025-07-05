from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        if not phone_number and not email:
            raise ValueError('The user must have either a phone number or an email address')
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

class CustomUser(AbstractUser):
    username = None  # Remove username field

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

    USERNAME_FIELD = 'phone_number'  # Use phone number for authentication
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email or 'no email'})"
