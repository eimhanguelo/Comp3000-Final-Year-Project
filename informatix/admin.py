from django.contrib import admin
from django import forms
from .models import Roster, ShiftPlan
from django.contrib.auth.models import User
from .forms import EngineerForm

class RosterAdminForm(forms.ModelForm):
    supervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),  # Only show staff users
        required=False,  # Make the supervisor field optional, if desired
        empty_label="Select Supervisor",  # Optional label for the empty option
        widget=forms.Select(attrs={'class': 'form-control'})  # Bootstrap class (optional)
    )

    class Meta:
        model = Roster
        fields = '__all__'  # Include all fields in the form


class ShiftPlan_Inline_admin(admin.TabularInline):
    model = ShiftPlan
    form = EngineerForm


class Roster_Admin(admin.ModelAdmin):
    form = RosterAdminForm  # Use the custom form for the Roster model
    list_display = ['name', 'id', 'is_active', 'supervisor', 'month']
    search_fields = ['name', 'id', 'supervisor__username']  # Search by name, id, or supervisor's username
    list_editable = ['is_active']
    list_filter = ['is_active', 'month']  # Filter by is_active and month
    ordering = ['-is_active', 'month']

    inlines = [ShiftPlan_Inline_admin]  # Inline ShiftPlan management

    def get_queryset(self, request):
        """Limit the queryset based on the logged-in user (if necessary)."""
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(supervisor=request.user)  # Only show rosters supervised by the logged-in user
        return queryset


admin.site.register(Roster, Roster_Admin)
