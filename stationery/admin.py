from django.contrib import admin
from .models import Stationery, Category, Variation, StationeryImage

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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'price_modifier')
    search_fields = ('name', 'value')
