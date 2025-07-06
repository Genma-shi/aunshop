from django.apps import AppConfig

def ready(self):
    import books.signals

class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'
    verbose_name = "Книги"