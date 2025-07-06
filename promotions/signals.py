from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Promotion
from users.models import CustomUser
from utils.notifications import send_fcm_notification

@receiver(post_save, sender=Promotion)
def notify_users_on_promotion_create(sender, instance, created, **kwargs):
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
                title="Новая акция!",
                body=f"{instance.title}: со скидкой с {instance.old_price} до {instance.new_price} сом!",
                fcm_token=user.fcm_token
            )

