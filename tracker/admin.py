# admin.py
from django.contrib import admin
from .models import Tracker
from simple_history.admin import SimpleHistoryAdmin
from users.admin import custom_admin_site

class TrackerAdmin(SimpleHistoryAdmin):
    list_display = ('category', 'created_by', 'created_at', 'updated_at')
    search_fields = ('category', 'description', 'remarks', 'created_by__username')
    list_filter = ('created_at', 'updated_at', 'created_by')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    history_list_display = ['history_id', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('created_by')

admin.site.register(Tracker, TrackerAdmin)
