from django.contrib import admin
from .models import Book, Subject
from users.models import CustomUser
from utils.notifications import send_fcm_notification

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'book_class', 'language', 'subject')
    list_filter = ('book_class', 'language', 'subject')
    search_fields = ('title', 'author')
    prepopulated_fields = {'description': ('title',)}

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # если книги ещё не было в базе
        super().save_model(request, obj, form, change)

        if is_new:
            users = CustomUser.objects.filter(
                notifications_enabled=True
            ).exclude(
                fcm_token__isnull=True
            ).exclude(
                fcm_token__exact=''
            )
            for user in users:
                try:
                    send_fcm_notification(
                        title="Новая книга!",
                        body=f"{obj.title} уже в наличии",
                        fcm_token=user.fcm_token
                    )
                except Exception as e:
                    print(f"[FCM] Ошибка при отправке пользователю {user.id}: {e}")

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
