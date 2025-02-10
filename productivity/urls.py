from django.urls import path, include
from .views import *

from . import views

urlpatterns = [

    #-----------------------------------------Suggestion Box---------------------------------------------------
    path('admin-suggestion-box', AdminSuggestionBoxView.as_view(), name='admin-suggestion-box'),
    path('user/<str:username>/suggestion_box', UserSuggestionBoxView.as_view(), name='user-suggestion-box'),

    #---------------------------------------Opoortunity Tag-----------------------------------------------------
    path('opportunity-tag/<int:pk>/', OpportunityTagDetailView.as_view(), name='opportunity-tag-detail'),
    path('opportunity-tag/new/', OpportunityTagCreateView.as_view(), name='opportunity-tag-create'),
    path('opportunity-tag/<int:pk>/update', OpportunityTagUpdateView.as_view(), name='opportunity-tag-update'),

    path('opportunity-tag/<int:pk>/admin/', OpportunityTagAdminCreateView.as_view(), name='opportunity-tag-admin-create'),
    path('opportunity-tag/<int:pk>/admin_update', OpportunityTagAdminUpdateView.as_view(), name='opportunity-tag-admin-update'),

    #---------------------------------------Observation Tag-----------------------------------------------------
    path('observation-tag/<int:pk>/', ObservationTagDetailView.as_view(), name='observation-tag-detail'),
    path('observation-tag/new/', ObservationTagCreateView.as_view(), name='observation-tag-create'),
    path('observation-tag/<int:pk>/update', ObservationTagUpdateView.as_view(), name='observation-tag-update'),

    path('observation-tag/<int:pk>/admin/', ObservationTagAdminCreateView.as_view(), name='observation-tag-admin-create'),
    path('observation-tag/<int:pk>/admin_update', ObservationTagAdminUpdateView.as_view(), name='observation-tag-admin-update'),

    # path('requisition/new/', RequisitionCreateView.as_view(), name='requisition-create'),
    # path('requisition/<int:pk>/update', RequisitionUpdateView.as_view(), name='requisition-update'),
    # path('requisition/<int:pk>/asset', RequisitionAssetCreateView.as_view(), name='asset-create'),
    # path('requisition/<int:pk>/sign', RequisitionSignCreateView.as_view(), name='req-sign-create'),
    # path('requisition/<int:pk>/pdf', RequisitionPDF.as_view(), name='requisition-pdf'),

    # #--------------------------------------Requisition Products-----------------------------------------------
    # path('requisition/<pk>/prod/', create_prod, name='prod-create'),
    # path('create_prod_form/', create_prod_form, name='create-prod-form'),
    # path('req_prod/<pk>/', detail_prod, name="detail-prod"),
    # path('req_prod/<pk>/update/', update_prod, name="update-prod"),
    # path('req_prod/<pk>/delete/', delete_prod, name="delete-prod"),

    # #--------------------------------------Inventory-----------------------------------------------
    # path('inventory', InventoryListView.as_view(), name='inventory-home'),

    # path('inventory/<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),
    # path('inventory/new/', InventoryCreateView.as_view(), name='inventory-create'),
    # path('inventory/<int:pk>/update', InventoryUpdateView.as_view(), name='inventory-update'),




    # -------------------------------------------------------------------------------------------------------
]
