from django.contrib import admin
from .models import PageContent
from django import forms

class PageContentAdminForm(forms.ModelForm):
    class Meta:
        model = PageContent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если это редактирование (instance есть и pk установлен), то делаем поле key readonly (запрет)
        if self.instance and self.instance.pk:
            self.fields['key'].disabled = True


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    form = PageContentAdminForm
    list_display = ('key', 'title')
    list_editable = ('title',)
    search_fields = ('key', 'title')

from django.contrib import admin
from django.contrib.auth.models import User, Group
from fcm_django.models import FCMDevice

for model in (User, Group, FCMDevice):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass
