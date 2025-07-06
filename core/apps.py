from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = "Общая информация"
    def ready(self):
        from django.contrib import admin
        from django.contrib.auth.models import User, Group
        from fcm_django.models import FCMDevice

        for model in (User, Group, FCMDevice):
            try:
                admin.site.unregister(model)
            except admin.sites.NotRegistered:
                pass
