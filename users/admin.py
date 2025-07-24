from django.contrib import admin
from .models import CustomUser, FCMDevice
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token

admin.site.register(FCMDevice)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')

    def delete_model(self, request, obj):
        # Удаляем все FCM токены, связанные с пользователем
        FCMDevice.objects.filter(user=obj).delete()

        # Удаляем все токены DRF Token для этого пользователя
        Token.objects.filter(user=obj).delete()

        # Удаляем самого пользователя
        super().delete_model(request, obj)

# Снимаем регистрацию ненужных моделей из админки
for model in (FCMDevice, Group, User):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass
