# stationery/apps.py
from django.apps import AppConfig

class StationeryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stationery'
    verbose_name = "Канцтовары"

    def ready(self):
        import stationery.signals  # подключаем сигнал
