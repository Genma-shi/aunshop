from django.contrib import admin
from .models import Stationery, Category, Variation, StationeryImage

@admin.register(Stationery)
class StationeryAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'brand', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'brand')
    filter_horizontal = ('images', 'variations')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'price_modifier')
    search_fields = ('name', 'value')

@admin.register(StationeryImage)
class StationeryImageAdmin(admin.ModelAdmin):
    list_display = ('image',)