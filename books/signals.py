from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book
from users.models import CustomUser
from fcm_django.models import FCMDevice

@receiver(post_save, sender=Book)
def send_new_book_notification(sender, instance, created, **kwargs):
    if created:
        users = CustomUser.objects.filter(fcm_token__isnull=False)
        devices = FCMDevice.objects.filter(user__in=users, active=True)
        if devices.exists():
            devices.send_message(
                title="Новая книга добавлена!",
                body=f"Ознакомьтесь с новой книгой: {instance.title}",
                data={"book_id": str(instance.id)},
            )