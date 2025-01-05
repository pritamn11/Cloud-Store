from django.contrib import admin
from .models import File
# Register your models here.

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'folder', 'file_type', 'size', 'location', 'created_at', 'updated_at')
    list_filter = ('user', 'file_type', 'created_at')
    search_fields = ('name', 'location', 'user__username', 'file_type')
    ordering = ('-created_at',)
    autocomplete_fields = ['folder', 'user']
    readonly_fields = ('location', 'created_at', 'updated_at')