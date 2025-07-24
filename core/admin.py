from django.contrib import admin
from .models import PageContent, ContactPhoneNumber
from django import forms
from django.contrib.auth.models import User, Group
from fcm_django.models import FCMDevice

class PageContentAdminForm(forms.ModelForm):
    class Meta:
        model = PageContent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['key'].disabled = True

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    form = PageContentAdminForm
    list_display = ('key', 'title')
    list_editable = ('title',)
    search_fields = ('key', 'title')

admin.site.register(ContactPhoneNumber)  # Оставляем отдельно

# Отключаем лишние модели
for model in (User, Group, FCMDevice):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass
