from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from users.admin import custom_admin_site

# Inline Admin Classes
class ProductModelInline(admin.TabularInline):
    model = ProductModel
    extra = 0


class RequisitionSignInline(admin.TabularInline):
    model = RequisitionSign
    extra = 0


class RequisitionHODInline(admin.TabularInline):
    model = RequisitionHOD
    extra = 0


class RequisitionHRInline(admin.TabularInline):
    model = RequisitionHR
    extra = 0



class RequisitionHODITInline(admin.TabularInline):
    model = RequisitionHODIT
    extra = 0


class RequisitionITInline(admin.TabularInline):
    model = RequisitionIT
    extra = 0


class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 0


# ModelAdmin Classes
@admin.register(Product)
class ProductAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'has_asset_no', 'transfer_list_item']
    search_fields = ['id', 'name', 'has_asset_no','transfer_list_item']
    history_list_display = ['history_id', ]
    inlines = [ProductModelInline]

admin.site.register(Product, ProductAdmin)

@admin.register(QuantityUnit)
class QuantityUnitAdmin(admin.ModelAdmin):
    pass


from simple_history.admin import SimpleHistoryAdmin

@admin.register(Requisition)
class RequisitionAdmin(SimpleHistoryAdmin):  # Inherit SimpleHistoryAdmin to handle history tracking
    list_display = ['get_form_id_req', 'id', 'author', 'requisition_no', 'date_posted', 'date_updated']
    search_fields = ['id', 'author__username']
    history_list_display = ['history_id', ]
    inlines = [
        InventoryInline, RequisitionSignInline, RequisitionHODInline,
        RequisitionHRInline, RequisitionHODITInline, RequisitionITInline,
    ]
    
    # Method to generate form_id
    def get_form_id_req(self, obj):
        # Assuming the form_id is constructed like this:
        return f"RQSN-{obj.id}/{obj.author.id}/{obj.author.profile.emp_id}"

    get_form_id_req.short_description = 'Form ID'  # Optional: Customize the column name in the admin

custom_admin_site.register(Requisition, RequisitionAdmin)







#------------------------------Inventory------------------------
class Inventory_Admin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ['product', 'id', 'model', 'product_condition', 'requisition', 'quantity', 'reference']
    search_fields = ['product__name', 'id', 'model__name', 'product_condition', 'requisition__id', 'quantity', 'reference']


admin.site.register(Inventory, Inventory_Admin)

admin.site.register(CostCenter)

#-------------------------------------------------------------
class PhoneHistoryAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ["mac_address", "department" , "ext", "display_name", "provided_ip", "date_updated"]
    # list_filter = ['vlan']
    search_fields = ["mac_address", "department__name", "ext", "display_name", "provided_ip", "date_updated"]

admin.site.register(Phone, PhoneHistoryAdmin)


class PhoneModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    search_fields = ['id', 'name']

admin.site.register(PhoneModel, PhoneModel_Admin)



admin.site.register(Test)




