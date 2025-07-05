from django.apps import AppConfig

def ready(self):
    import books.signals
