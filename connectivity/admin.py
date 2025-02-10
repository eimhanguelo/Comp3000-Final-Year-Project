from django.contrib import admin
from .models import *

from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin


@admin.register(LanTransferInstrument)
class LanTransferInstrumentAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ('id', 'author', 'current_ip_address', 'current_location', 'current_floor', 'current_department', 'new_location', 'new_floor', 'new_department', 'date_posted', 'date_updated')
    list_filter = ('current_location', 'current_floor', 'current_department', 'new_location', 'new_floor', 'new_department', 'author')
    search_fields = ('purpose_of_transfer', 'author__username', 'author__profile__emp_id')
    readonly_fields = ('date_posted', 'date_updated')
    fieldsets = (
        (None, {
            'fields': ('author', 'current_ip_address', 'current_location', 'current_floor', 'current_department', 'new_location', 'new_floor', 'new_department', 'purpose_of_transfer', 'recommended_hod', 'recommended_hr')
        }),
        ('Dates', {
            'fields': ('date_posted', 'date_updated'),
            'classes': ('collapse',),
        }),
    )
    filter_horizontal = ('recommended_hr',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('recommended_hr',)
        return self.readonly_fields
# Register your models here.
#-------------------------------------------------------------
class OSAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]
    list_filter = ['name']
    ordering = ['id']  # Default order

admin.site.register(OS, OSAdmin)

#-------------------------------------------------------------
class SwitchAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]
    list_filter = ['name']
    ordering = ['id']  # Default order

admin.site.register(Switch, SwitchAdmin)

#-------------------------------------------------------------
class CPUAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]
    list_filter = ['name']
    ordering = ['id']  # Default order
admin.site.register(CentralProcessingUnit, CPUAdmin)
# #-------------------------------------------------------------
class PrinterAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]
    list_filter = ['name']
    ordering = ['id']  # Default order
admin.site.register(PrinterModel, PrinterAdmin)

# #-------------------------------------------------------------
class ScannerAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]
    list_filter = ['name']
    ordering = ['id']  # Default order
admin.site.register(ScannerModel, ScannerAdmin)



#-------------------------------------------------------------
class LanHistoryAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ["ip_address", "computer_name", "vlan", "switch_name"]
    list_filter = ['vlan']
    search_fields = ['ip_address', 'computer_name', 'vlan', 'switch_name__name']

admin.site.register(Lan, LanHistoryAdmin)

#--------------------------------Lan Request Admin Section-----------------------------------

class LanRequest_Sign_InLine_Admin(admin.TabularInline):
    model = LanRequestSign
    extra = 0

class LanRequest_IT_InLine_Admin(admin.TabularInline):
    model = LanRequestIT
    extra = 0
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import LanRequest

class LanRequest_Admin(SimpleHistoryAdmin):  # Use SimpleHistoryAdmin to handle history
    list_display = ['get_form_id_lanreq', 'id', 'author', 'date_posted', 'date_updated']
    search_fields = ['id', 'author__username']
    history_list_display = ['history_id', ]
    inlines = [LanRequest_Sign_InLine_Admin, LanRequest_IT_InLine_Admin]

    # Method to generate form_id
    def get_form_id_lanreq(self, obj):
        # Assuming the form_id is constructed like this:
        return f"LCRF-{obj.id}/{obj.author.id}/{obj.author.profile.emp_id}"

    get_form_id_lanreq.short_description = 'Form ID'  # Optional: Customize the column name in the admin

admin.site.register(LanRequest, LanRequest_Admin)


#--------------------------------Lan Transfer Admin Section-----------------------------------


class LanTransfer_HOD_InLine_Admin(admin.TabularInline):
    model = LanTransferHOD
    extra = 0

class LanTransfer_HR_InLine_Admin(admin.TabularInline):
    model = LanTransferHR
    extra = 0

class LanTransfer_IT_InLine_Admin(admin.TabularInline):
    model = LanTransferIT
    extra = 0

class LanTransfer_Admin(SimpleHistoryAdmin):
    list_display = ['get_form_id_lantransfer','id', 'author', 'date_posted', 'date_updated']
    search_fields = ['id', 'author__username']
    history_list_display = ['history_id', ]
    inlines = [LanTransfer_HOD_InLine_Admin, 
                LanTransfer_HR_InLine_Admin, LanTransfer_IT_InLine_Admin]

    def get_form_id_lantransfer(self, obj):
        # Assuming the form_id is constructed like this:
        return f"LCTF-{obj.id}/{obj.author.id}/{obj.author.profile.emp_id}"

    get_form_id_lantransfer.short_description = 'Form ID'  # Optional: Customize the column name in the admin

admin.site.register(LanTransfer, LanTransfer_Admin)

#--------------------------------Lan Transfer Admin Section-----------------------------------

class LanInstrument_Sign_InLine_Admin(admin.TabularInline):
    model = LanInstrumentSign
    extra = 0

class LanInstrument_IT_InLine_Admin(admin.TabularInline):
    model = LanInstrumentIT
    extra = 0

class LanInstrument_Admin(SimpleHistoryAdmin):
    list_display = ['get_form_id_lan_ins_con','id', 'author', 'date_posted', 'date_updated']
    search_fields = ['id', 'author__username']
    history_list_display = ['history_id', ]
    inlines = [LanInstrument_Sign_InLine_Admin, LanInstrument_IT_InLine_Admin]


    def get_form_id_lan_ins_con(self, obj):
        # Assuming the form_id is constructed like this:
        return f"RILC-{obj.id}/{obj.author.id}/{obj.author.profile.emp_id}"

    get_form_id_lan_ins_con.short_description = 'Form ID'  # Optional: Customize the column name in the admin

admin.site.register(LanInstrument, LanInstrument_Admin)

#--------------------------------Lan Transfer Admin Section-----------------------------------

class LanTransferInstrument_Sign_InLine_Admin(admin.TabularInline):
    model = LanTransferInstrumentHOD
    extra = 0

class LanTransferInstrument_HR_InLine_Admin(admin.TabularInline):
    model = LanTransferInstrumentHR
    extra = 0

class LanTransferInstrument_IT_InLine_Admin(admin.TabularInline):
    model = LanTransferInstrumentIT
    extra = 0

class LanTransferInstrument_Admin(SimpleHistoryAdmin):
    list_display = ['get_form_id_lan_ins_trns','id','author', 'date_posted', 'date_updated']
    search_fields = ['id', 'author__username']
    history_list_display = ['history_id', ]
    inlines = [LanTransferInstrument_Sign_InLine_Admin,LanTransferInstrument_HR_InLine_Admin, LanTransferInstrument_IT_InLine_Admin]

    def get_form_id_lan_ins_trns(self, obj):
        # Assuming the form_id is constructed like this:
        return f"ILCT-{obj.id}/{obj.author.id}/{obj.author.profile.emp_id}"

    get_form_id_lan_ins_trns.short_description = 'Form ID'  # Optional: Customize the column name in the admin

admin.site.register(LanTransferInstrument, LanTransferInstrument_Admin)

# class Internet_HOD_InLine_Admin(admin.TabularInline):
#     model = InternetHOD
#     extra = 0

# class Internet_HR_InLine_Admin(admin.TabularInline):
#     model = InternetHR
#     extra = 0

# class Internet_IT_InLine_Admin(admin.TabularInline):
#     model = InternetIT
#     extra = 0

# class Internet_Admin(admin.ModelAdmin):
#     list_display = ['id', 'author']
#     search_fields = ['id', 'author__username']

#     inlines = [Internet_HOD_InLine_Admin, Internet_HR_InLine_Admin, Internet_IT_InLine_Admin]

# admin.site.register(Internet, Internet_Admin)

#--------------------------------Permission Admin Section-----------------------------------

# class Permission_HOD_InLine_Admin(admin.TabularInline):
#     model = PermissionHOD
#     extra = 0

# class Permission_HR_InLine_Admin(admin.TabularInline):
#     model = PermissionHR
#     extra = 0

# class Permission_IT_InLine_Admin(admin.TabularInline):
#     model = PermissionIT
#     extra = 0

# class Permission_Admin(admin.ModelAdmin):
#     list_display = ['id', 'author']
#     search_fields = ['id', 'author__username']

#     inlines = [Permission_HOD_InLine_Admin, Permission_HR_InLine_Admin, Permission_IT_InLine_Admin]

# admin.site.register(Permission, Permission_Admin)

#--------------------------------File Access Admin Section-----------------------------------

class Link_InLine_Admin(admin.TabularInline):
    model = FileLink
    extra = 0
class FileAccess_Sign_InLine_Admin(admin.TabularInline):
    model = FileAccessSign
    extra = 0

class FileAccess_Admin(SimpleHistoryAdmin):

    list_display = ['get_form_id_dfs','id','author', 'date_posted', 'date_updated']
    search_fields = ['id', 'author__username']
    history_list_display = ['history_id', ]
    
    inlines = [Link_InLine_Admin, FileAccess_Sign_InLine_Admin]

    def get_form_id_dfs(self, obj):
        # Assuming the form_id is constructed like this:
        return f"FSAF-{obj.id}/{obj.author.id}/{obj.author.profile.emp_id}"

    get_form_id_dfs.short_description = 'Form ID'  # Optional: Customize the column name in the admin

admin.site.register(FileAccess, FileAccess_Admin)

# #--------------------------------Requisition Admin Section-----------------------------------

# class Products_InLine_Admin(admin.TabularInline):
#     model = RequisitionProducts
#     extra = 0
# class Requisition_Sign_InLine_Admin(admin.TabularInline):
#     model = RequisitionSign
#     extra = 0

# class Requisition_Admin(admin.ModelAdmin):
#     inlines = [Products_InLine_Admin, Requisition_Sign_InLine_Admin]

# admin.site.register(Requisition, Requisition_Admin)

