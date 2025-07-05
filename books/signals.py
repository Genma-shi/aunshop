# books/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book
from users.models import CustomUser  # кто получит
from utils.notifications import send_fcm_notification

@receiver(post_save, sender=Book)
def notify_on_book_create(sender, instance, created, **kwargs):
    if created:
        users = CustomUser.objects.exclude(fcm_token__isnull=True).exclude(fcm_token__exact='')
        for user in users:
            send_fcm_notification(
                title="📚 Новая книга!",
                body=f"{instance.title} уже в наличии",
                fcm_token=user.fcm_token
            )
