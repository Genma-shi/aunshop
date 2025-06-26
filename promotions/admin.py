from django.contrib import admin
from .models import Promotion, PromotionImage

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'old_price', 'new_price')
    search_fields = ('title', 'description')
    filter_horizontal = ('images',)

@admin.register(PromotionImage)
class PromotionImageAdmin(admin.ModelAdmin):
    list_display = ('image',)