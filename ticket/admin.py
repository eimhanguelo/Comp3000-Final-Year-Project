from django.contrib import admin
from .models import (
    EInternal, Eticket, EAssign, ESolve, EDiscussion,
    ProblemCategory, AuditTrail
)
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from users.admin import custom_admin_site

# Register the ProblemCategory model
class ProblemCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'problem_name']
    search_fields = ['id', 'problem_name']

admin.site.register(ProblemCategory, ProblemCategoryAdmin)

# Inlines for Eticket
class EAssignInlineAdmin(admin.TabularInline):
    model = EAssign
    extra = 0

class EDiscussionInlineAdmin(admin.TabularInline):
    model = EDiscussion
    extra = 0

class EInternalInlineAdmin(admin.TabularInline):
    model = EInternal
    extra = 0

class ESolveInlineAdmin(admin.TabularInline):
    model = ESolve
    extra = 0

# Eticket Admin
class EticketAdmin(SimpleHistoryAdmin):  # Use SimpleHistoryAdmin for historical tracking
    list_display = ['ticket_id', 'id', 'ticket_raiser', 'status', 'ticket_engineer','date_raised']
    search_fields = ['id', 'ticket_raiser__username', 'status']
    list_filter = ('ticket_raiser', 'status', 'ticket_engineer','date_raised')  
    inlines = [EAssignInlineAdmin, ESolveInlineAdmin, EDiscussionInlineAdmin, EInternalInlineAdmin]

    def ticket_id(self, obj: Eticket) -> str:
        """
        Custom method to generate a formatted ticket ID for display in the admin.
        """
        emp_id = getattr(obj.ticket_raiser.profile, 'emp_id', 'Unknown')
        return f"ETCKT-{obj.id}/{obj.ticket_raiser.id}/{emp_id}"

# Register Eticket with custom admin site
custom_admin_site.register(Eticket, EticketAdmin)

# AuditTrail Admin
class AuditTrailAdmin(SimpleHistoryAdmin):
    list_display = ('ticket', 'id', 'action_type', 'performed_by', 'performed_at', 'details')
    list_filter = ('action_type', 'performed_at', 'performed_by')  # Filters by action type, time, and user
    search_fields = ('ticket__id', 'performed_by__username', 'details')  # Search by ticket ID, user, and details
    ordering = ('-performed_at',)  # Order by 'performed_at', most recent first

# Register the AuditTrail model
admin.site.register(AuditTrail, AuditTrailAdmin)
