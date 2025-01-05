from django.contrib import admin
from .models import Folder
# Register your models here.

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'parent_folder', 'location', 'type', 'created_at', 'updated_at')
    list_filter = ('user', 'type', 'created_at')
    search_fields = ('name', 'location', 'user__username')
    ordering = ('-created_at',)
    autocomplete_fields = ['parent_folder', 'user']
    readonly_fields = ('location', 'created_at', 'updated_at')