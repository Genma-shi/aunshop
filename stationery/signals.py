from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Stationery
from users.models import CustomUser
from utils.notifications import send_fcm_notification

@receiver(post_save, sender=Stationery)
def notify_users_on_stationery_create(sender, instance, created, **kwargs):
    if created:
        users = CustomUser.objects.filter(
            notifications_enabled=True
        ).exclude(
            fcm_token__isnull=True
        ).exclude(
            fcm_token__exact=''
        )
        for user in users:
            send_fcm_notification(
                title="Новый товар в канцелярии!",
                body=f"{instance.title} — {instance.price} сом. {instance.description[:50]}...",
                fcm_token=user.fcm_token
            )


