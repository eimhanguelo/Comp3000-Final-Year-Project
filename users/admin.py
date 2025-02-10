from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from simple_history import register
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from django import forms
from django.db.models import Q
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.response import TemplateResponse
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Department, Position, Location, Floor, Profile
from users.utils import sync_ldap_users

# ----------------------------------------------
# Custom Admin Site
# ----------------------------------------------

class CustomAdminSite(admin.AdminSite):
    site_header = "Admin Dashboard"
    site_title = "Admin Portal"
    index_title = "Welcome to the Admin Portal"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync-ldap-users/', self.admin_view(self.sync_ldap_users), name='sync-ldap-users'),
        ]
        return custom_urls + urls

    def sync_ldap_users(self, request):
        """Sync users with LDAP."""
        result = sync_ldap_users()
        if result["status"] == "success":
            messages.success(request, "LDAP synchronization completed successfully!")
        else:
            messages.error(request, f"Error during LDAP sync: {result['message']}")
        return HttpResponseRedirect('/admin/')

    def index(self, request, extra_context=None):
        """Customize the admin index page."""
        extra_context = extra_context or {}
        extra_context['show_sync_button'] = True
        return super().index(request, extra_context=extra_context)


# Replace default admin site with the custom admin site
custom_admin_site = CustomAdminSite(name="custom_admin")
admin.site = custom_admin_site

# Register built-in models
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Group, GroupAdmin)

# ----------------------------------------------
# Department, Position, Location, and Floor Admins
# ----------------------------------------------

class BaseAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    """Base class for common admin configurations."""
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_filter = ['name']
    ordering = ['id']


@admin.register(Department, site=custom_admin_site)
class DepartmentAdmin(BaseAdmin):
    pass


@admin.register(Position, site=custom_admin_site)
class PositionAdmin(BaseAdmin):
    pass


@admin.register(Location, site=custom_admin_site)
class LocationAdmin(BaseAdmin):
    pass


@admin.register(Floor, site=custom_admin_site)
class FloorAdmin(BaseAdmin):
    pass

# ----------------------------------------------
# Profile Admin with Custom Form and Filters
# ----------------------------------------------

class ProfileForm(forms.ModelForm):
    """Custom form for the Profile model."""
    class Meta:
        model = Profile
        fields = '__all__'

    recom_permission_departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=FilteredSelectMultiple("Recom Permission Departments", is_stacked=False),
        required=False,
    )
    recom_permission_locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.all(),
        widget=FilteredSelectMultiple("Recom Permission Locations", is_stacked=False),
        required=False,
    )
    hod_permission_departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=FilteredSelectMultiple("HOD Permission Departments", is_stacked=False),
        required=False,
    )
    hod_permission_locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.all(),
        widget=FilteredSelectMultiple("HOD Permission Locations", is_stacked=False),
        required=False,
    )


# Custom filters for ManyToMany fields
class BasePermissionFilter(admin.SimpleListFilter):
    """Base class for permission filters."""
    def lookups(self, request, model_admin):
        return [(obj.id, obj.name) for obj in self.model.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{f"{self.parameter_name}__id": self.value()})
        return queryset


class RecomPermissionDepartmentFilter(BasePermissionFilter):
    title = "Recom Permission Department"
    parameter_name = "recom_permission_departments"
    model = Department


class RecomPermissionLocationFilter(BasePermissionFilter):
    title = "Recom Permission Location"
    parameter_name = "recom_permission_locations"
    model = Location


class HODPermissionDepartmentFilter(BasePermissionFilter):
    title = "HOD Permission Department"
    parameter_name = "hod_permission_departments"
    model = Department


class HODPermissionLocationFilter(BasePermissionFilter):
    title = "HOD Permission Location"
    parameter_name = "hod_permission_locations"
    model = Location


# Profile Admin
@admin.register(Profile, site=custom_admin_site)
class ProfileHistoryAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    """Admin for the Profile model."""
    form = ProfileForm
    list_display = [
        'user', 'user_first_name', 'emp_id', 'department', 'position',
        'is_hr', 'is_accountant', 'is_verifier_it', 'is_hod_it',
        'display_recom_permission_departments', 'display_recom_permission_locations',
        'display_hod_permission_departments', 'display_hod_permission_locations'
    ]
    search_fields = ['user__username', 'user__first_name', 'emp_id', 'department__name', 'position__name']
    list_filter = [
        'department', 'position', 'is_hr', 'is_accountant', 'is_verifier_it', 'is_hod_it',
        HODPermissionDepartmentFilter, HODPermissionLocationFilter,
        RecomPermissionDepartmentFilter, RecomPermissionLocationFilter
    ]
    ordering = ['user__first_name']
    history_list_display = ['history_id', ]

    @admin.display(ordering='user__first_name')
    def user_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description="Recom Departments")
    def display_recom_permission_departments(self, obj):
        return ", ".join([dept.name for dept in obj.recom_permission_departments.all()])

    @admin.display(description="Recom Locations")
    def display_recom_permission_locations(self, obj):
        return ", ".join([loc.name for loc in obj.recom_permission_locations.all()])

    @admin.display(description="HOD Departments")
    def display_hod_permission_departments(self, obj):
        return ", ".join([dept.name for dept in obj.hod_permission_departments.all()])

    @admin.display(description="HOD Locations")
    def display_hod_permission_locations(self, obj):
        return ", ".join([loc.name for loc in obj.hod_permission_locations.all()])


# Register the User model for history tracking
register(User)
