from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Group, User
from fcm_django.models import FCMDevice

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')

for model in (FCMDevice, Group, User):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass