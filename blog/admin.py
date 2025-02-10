from django.contrib import admin
from .models import *
from django.utils.html import format_html

from simple_history import register
from simple_history.admin import SimpleHistoryAdmin

from users.admin import custom_admin_site


# Register your models here.
class Employee_Sign_InLine_Admin(admin.TabularInline):
    model = EmployeeSign
    extra = 0

class Employee_HOD_InLine_Admin(admin.TabularInline):
    model = EmployeeHOD
    extra = 0

class Employee_HR_InLine_Admin(admin.TabularInline):
    model = EmployeeHR
    extra = 0

class Employee_IT_InLine_Admin(admin.TabularInline):
    model = EmployeeIT
    extra = 0

from simple_history.admin import SimpleHistoryAdmin

class Employee_Admin(SimpleHistoryAdmin):
    list_display = ['get_form_id_emp', 'id', 'author', 'date_posted', 'date_updated'] 
    search_fields = ['id', 'author__username']
    inlines = [Employee_Sign_InLine_Admin, Employee_HOD_InLine_Admin, Employee_HR_InLine_Admin, Employee_IT_InLine_Admin]
    history_list_display = ['history_id', ]

    # Method to generate form_id
    def get_form_id_emp(self, obj):
        # Assuming the form_id is constructed like this:
        return f"HR-{obj.id}/{obj.author.id}/{obj.author.profile.emp_id}"

    get_form_id_emp.short_description = 'Form ID'  # Optional: Customize the column name in the admin

custom_admin_site.register(Employee, Employee_Admin)


#--------------------------------Account Admin Section-----------------------------------

class Account_Sign_InLine_Admin(admin.TabularInline):
    model = AccountSign
    extra = 0

class Account_HOD_InLine_Admin(admin.TabularInline):
    model = AccountHOD
    extra = 0

class Account_HR_InLine_Admin(admin.TabularInline):
    model = AccountHR
    extra = 0

class Account_IT_InLine_Admin(admin.TabularInline):
    model = AccountIT
    extra = 0

# Admin class for Account model
class Account_Admin(SimpleHistoryAdmin, admin.ModelAdmin):
    # Define the fields to be shown in the list display
    list_display = ['get_form_id_acc', 'id', 'author', 'date_posted', 'date_updated']  # Add get_form_id to list_display
    search_fields = ['id', 'author__username']  # Enable searching by 'id' and 'author'
    
    # Inlines for related models
    inlines = [
        Account_Sign_InLine_Admin, 
        Account_HOD_InLine_Admin, 
        Account_HR_InLine_Admin, 
        Account_IT_InLine_Admin
    ]

    history_list_display = ['history_id', ]
    
    # Method to generate form_id dynamically
    def get_form_id_acc(self, obj):
        # Ensure the author has a profile and emp_id attribute available
        return f"MUAC-{obj.id}/{obj.author.id}/{obj.author.profile.emp_id}"

    get_form_id_acc.short_description = 'Form ID'  # Set the name for the column header in admin

custom_admin_site.register(Account, Account_Admin)

#--------------------------------IT Release Admin Section-----------------------------------
# Uncomment the following code if needed
# class Resignation_Data_InLine_Admin(admin.TabularInline):
#     model = ResignationData
#     extra = 0

# class Resignation_Admin(admin.ModelAdmin):
#     inlines = [Resignation_Data_InLine_Admin]

# custom_admin_site.register(Resignation, Resignation_Admin)
