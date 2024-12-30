from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import User

# Register your models here.

class UserAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'created_at', 'updated_at']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['is_active', 'is_staff']
    readonly_fields = ['get_history_user', 'get_history_date', 'get_history_change_reason']

    def get_history_user(self, obj):
        # Accessing the historical user information
        if obj.history.exists():
            return obj.history.first().history_user
        return None

    def get_history_date(self, obj):
        # Accessing the history date
        if obj.history.exists():
            return obj.history.first().history_date
        return None

    def get_history_change_reason(self, obj):
        # Accessing the change reason
        if obj.history.exists():
            return obj.history.first().history_change_reason
        return None

    get_history_user.short_description = 'History User'
    get_history_date.short_description = 'History Date'
    get_history_change_reason.short_description = 'History Change Reason'

admin.site.register(User, UserAdmin)