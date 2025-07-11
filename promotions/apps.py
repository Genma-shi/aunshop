# promotions/apps.py
from django.apps import AppConfig

class PromotionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'promotions'
    verbose_name = "Акций"

    def ready(self):
        import promotions.signals  # подключение сигналов
