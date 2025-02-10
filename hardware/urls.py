from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Importing necessary class-based views
from .views import (
    RequisitionDetailView, RequisitionCreateView, RequisitionUpdateView,
    RequisitionSignCreateView, RequisitionSignUpdateView, RequisitionHODCreateView,
    RequisitionHODUpdateView, RequisitionHRCreateView, RequisitionHRUpdateView,
    RequisitionACCCreateView, RequisitionACCUpdateView, RequisitionVERIFYCreateView,
    RequisitionVERIFYUpdateView, RequisitionHODITCreateView, RequisitionHODITUpdateView,
    RequisitionITCreateView, RequisitionITUpdateView, RequisitionPDF,
    InventoryListView, InventoryDetailView, InventoryCreateView, InventoryUpdateView,
    InventoryStockView, PhoneListView, PhoneDetailView, PhoneCreateView, PhoneUpdateView,
    create_prod, create_prod_form, detail_prod, update_prod, delete_prod,
    load_models, display_requisition, send_email, display_name_hod, display_name_recommender
)

urlpatterns = [
    #---------------------------------------Requisition-----------------------------------------------------
    path('display_name_hod/', views.display_name_hod, name='display_name_hod'),
    path('display_name_recommender/', views.display_name_recommender, name='display_name_recommender'),

    path('requisition/<int:pk>/', RequisitionDetailView.as_view(), name='requisition-detail'),
    path('requisition/new/', RequisitionCreateView.as_view(), name='requisition-create'),
    path('requisition/<int:pk>/update/', RequisitionUpdateView.as_view(), name='requisition-update'),

    path('requisition/<int:pk>/sign/', RequisitionSignCreateView.as_view(), name='req-sign-create'),
    path('requisition/<int:pk>/sign_update/', RequisitionSignUpdateView.as_view(), name='req-sign-update'),

    path('requisition/<int:pk>/hod/', RequisitionHODCreateView.as_view(), name='req-hod-create'),
    path('requisition/<int:pk>/hod_update/', RequisitionHODUpdateView.as_view(), name='req-hod-update'),

    path('requisition/<int:pk>/hr/', RequisitionHRCreateView.as_view(), name='req-hr-create'),
    path('requisition/<int:pk>/hr_update/', RequisitionHRUpdateView.as_view(), name='req-hr-update'),

    path('requisition/<int:pk>/acc/', RequisitionACCCreateView.as_view(), name='req-acc-create'),
    path('requisition/<int:pk>/acc_update/', RequisitionACCUpdateView.as_view(), name='req-acc-update'),

    path('requisition/<int:pk>/itverify/', RequisitionVERIFYCreateView.as_view(), name='req-verify-create'),
    path('requisition/<int:pk>/itverify_update/', RequisitionVERIFYUpdateView.as_view(), name='req-verify-update'),

    path('requisition/<int:pk>/hod_it/', RequisitionHODITCreateView.as_view(), name='req-hod-it-create'),
    path('requisition/<int:pk>/hod_it_update/', RequisitionHODITUpdateView.as_view(), name='req-hod-it-update'),

    path('requisition/<int:pk>/it/', RequisitionITCreateView.as_view(), name='req-it-create'),
    path('requisition/<int:pk>/it_update/', RequisitionITUpdateView.as_view(), name='req-it-update'),

    path('requisition/<int:pk>/pdf/', RequisitionPDF.as_view(), name='requisition-pdf'),

    #--------------------------------------Requisition Products-----------------------------------------------
    path('requisition/<int:pk>/prod/', create_prod, name='prod-create'),
    path('create_prod_form/', create_prod_form, name='create-prod-form'),
    path('req_prod/<int:pk>/', detail_prod, name="detail-prod"),
    path('req_prod/<int:pk>/update/', update_prod, name="update-prod"),
    path('req_prod/<int:pk>/delete/', delete_prod, name="delete-prod"),

    path('requisition/send_email/<int:requisition_id>/', views.send_email, name='send_email'),

    #--------------------------------------Inventory-----------------------------------------------
    path('inventory/', InventoryListView.as_view(), name='inventory-home'),
    path('inventory/<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),
    path('inventory/new/', InventoryCreateView.as_view(), name='inventory-create'),
    path('inventory/<int:pk>/update/', InventoryUpdateView.as_view(), name='inventory-update'),
    path('inventory/stock_summary/', InventoryStockView.as_view(), name='stock-summary'),

    #--------------------------------------Phone-----------------------------------------------
    path('phone/', PhoneListView.as_view(), name='phone-home'),
    path('phone/<int:pk>/', PhoneDetailView.as_view(), name='phone-detail'),
    path('phone/new/', PhoneCreateView.as_view(), name='phone-create'),
    path('phone/<int:pk>/update/', PhoneUpdateView.as_view(), name='phone-update'),

    #--------------------------------------Load Models based on Products-----------------------------------------------
    path('load_models/', load_models, name='load-models'),
    path('display_requisition/', display_requisition, name='display_requisition'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
