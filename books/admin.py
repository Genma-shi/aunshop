from django.contrib import admin
from .models import Book, Subject

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'book_class', 'language', 'subject')
    list_filter = ('book_class', 'language', 'subject')
    search_fields = ('title', 'author')
    prepopulated_fields = {'description': ('title',)}

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)