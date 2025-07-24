from django.contrib import admin
from .models import Stationery, Category, Variation, StationeryImage
from users.models import CustomUser
from utils.notifications import send_fcm_notification

class StationeryImageInline(admin.TabularInline):
    model = StationeryImage
    extra = 1

@admin.register(Stationery)
class StationeryAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'brand', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'brand')
    filter_horizontal = ('variations',)
    inlines = [StationeryImageInline]

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
                        title="🖊️ Новый товар в канцелярии!",
                        body=f"{obj.title} уже в продаже за {obj.price} сом!",
                        fcm_token=user.fcm_token
                    )
                except Exception as e:
                    print(f"[FCM] Ошибка при отправке пользователю {user.id}: {e}")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'price_modifier')
    search_fields = ('name', 'value')
