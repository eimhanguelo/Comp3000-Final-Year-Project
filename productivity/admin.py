from django.contrib import admin
from .models import *

# Register your models here.
#----------------------------------Opportunity Tag Admin----------------------------
class OpportunityTag_InLine_Admin(admin.TabularInline):
    model = OpportunityTagAdmin
    extra = 0


class OpportunityTag_Admin(admin.ModelAdmin):
    list_display = ['title', 'author', 'idea_giver', 'date_updated']
    search_fields = ['id', 'title', 'author__username', 'idea_giver__username', 'date_updated']

    inlines = [OpportunityTag_InLine_Admin]

admin.site.register(OpportunityTag, OpportunityTag_Admin)


#----------------------------------Opportunity Tag Admin----------------------------
class ObservationTag_InLine_Admin(admin.TabularInline):
    model = ObservationTagAdmin
    extra = 0


class ObservationTag_Admin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_updated']
    search_fields = ['id', 'title', 'date_updated']

    inlines = [ObservationTag_InLine_Admin]

admin.site.register(ObservationTag, ObservationTag_Admin)