from django.contrib import admin
from .models import Promotion, PromotionImage
from users.models import CustomUser
from utils.notifications import send_fcm_notification

class PromotionImageInline(admin.TabularInline):
    model = PromotionImage
    extra = 1

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'old_price', 'new_price')
    search_fields = ('title', 'description')
    inlines = [PromotionImageInline]

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
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
                        title="🔥 Новая акция!",
                        body=f"{obj.title}: теперь всего за {obj.new_price}!",
                        fcm_token=user.fcm_token
                    )
                except Exception as e:
                    print(f"[FCM] Ошибка при отправке пользователю {user.id}: {e}")

@admin.register(PromotionImage)
class PromotionImageAdmin(admin.ModelAdmin):
    list_display = ('image',)
