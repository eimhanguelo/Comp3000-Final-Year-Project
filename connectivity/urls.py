from django.urls import path, include
from .views import *

from . import views
# Import the custom 403 view
from .views import custom_403_view

# Define the handler for 403 errors
handler403 = custom_403_view
urlpatterns = [

    #---------------------------------------Lan-------------------------------------------------------------
    path('lan/<int:pk>/', LanDetailView.as_view(), name='lan-detail'),

    path('lan/new/', LanCreateView.as_view(), name='lan-create'),
    path('lan/<int:pk>/update', LanUpdateView.as_view(), name='lan-update'),
 
    #-------------------------------------------------------------------------------------------------------

    #---------------------------------------LanRequest------------------------------------------------------
    path('lanrequest/<int:pk>/', LanRequestDetailView.as_view(), name='lan1-detail'),

    path('lanrequest/new/', LanRequestCreateView.as_view(), name='lan1-create'),
    path('lanrequest/<int:pk>/update', LanRequestUpdateView.as_view(), name='lan1-update'),

    path('lanrequest/<int:pk>/sign', LanRequestSignCreateView.as_view(), name='lan1sign-create'),
    path('lanrequest/<int:pk>/sign_update', LanRequestSignUpdateView.as_view(), name='lan1sign-update'),

    path('lanrequest/<int:pk>/it_sign', LanRequestITCreateView.as_view(), name='lan1it-create'),
    path('lanrequest/<int:pk>/it_sign_update', LanRequestITUpdateView.as_view(), name='lan1it-update'),
    path('lanrequest/<int:pk>/pdf', LanRequestPDF.as_view(), name='lan1-pdf'),

    #-------------------------------------------------------------------------------------------------------

    #---------------------------------------Lan Transfer----------------------------------------------------
    path('lantransfer/<int:pk>/', LanTransferDetailView.as_view(), name='lan2-detail'),

    path('lantransfer/new/', LanTransferCreateView.as_view(), name='lan2-create'),
    path('lantransfer/<int:pk>/update', LanTransferUpdateView.as_view(), name='lan2-update'),

    path('lantransfer/<int:pk>/hod_sign', LanTransferHODCreateView.as_view(), name='lan2hod-create'),
    path('lantransfer/<int:pk>/hod_sign_update', LanTransferHODUpdateView.as_view(), name='lan2hod-update'),

    path('lantransfer/<int:pk>/hr_sign', LanTransferHRCreateView.as_view(), name='lan2hr-create'),
    path('lantransfer/<int:pk>/hr_sign_update', LanTransferHRUpdateView.as_view(), name='lan2hr-update'),

    path('lantransfer/<int:pk>/it_sign', LanTransferITCreateView.as_view(), name='lan2it-create'),
    path('lantransfer/<int:pk>/it_sign_update', LanTransferHODCreateView.as_view(), name='lan2it-update'),

    path('lantransfer/<int:pk>/pdf', LanTransferPDF.as_view(), name='lan2-pdf'),
    #-------------------------------------------------------------------------------------------------------

    #---------------------------------------Lan Instrument--------------------------------------------------
    path('laninstrument/<int:pk>/', LanInstrumentDetailView.as_view(), name='lan3-detail'),
    path('laninstrument/new/', LanInstrumentCreateView.as_view(), name='lan3-create'),
    path('laninstrument/<int:pk>/update', LanInstrumentUpdateView.as_view(), name='lan3-update'),
    path('laninstrument/<int:pk>/sign', LanInstrumentSignCreateView.as_view(), name='lan3sign-create'),
    path('laninstrument/<int:pk>/sign_update', LanInstrumentSignUpdateView.as_view(), name='lan3sign-update'),
    path('laninstrument/<int:pk>/it_sign', LanInstrumentITCreateView.as_view(), name='lan3it-create'),
    path('laninstrument/<int:pk>/it_sign_update', LanInstrumentITUpdateView.as_view(), name='lan3it-update'),
    path('laninstrument/<int:pk>/pdf', LanInstrumentPDF.as_view(), name='lan3-pdf'),
    #-------------------------------------------------------------------------------------------------------

    #---------------------------------------Lan Transfer Instrument----------------------------------------------------
    path('lantransferinstrument/<int:pk>/', LanTransferInstrumentDetailView.as_view(), name='lantransferinstrument-detail'),
    path('lantransferinstrument/new/', LanTransferInstrumentCreateView.as_view(), name='lantransferinstrument-create'),
    path('lantransferinstrument/<int:pk>/update/', LanTransferInstrumentUpdateView.as_view(), name='lantransferinstrument-update'),
    path('lantransferinstrument/<int:pk>/hod_sign/', LanTransferInstrumentHODCreateView.as_view(), name='lantransferinstrument_hod-create'),
    path('lantransferinstrument/<int:pk>/hod_sign_update/', LanTransferInstrumentHODUpdateView.as_view(), name='lantransferinstrument_hod-update'),
    path('lantransferinstrument/<int:pk>/hr_sign/', LanTransferInstrumentHRCreateView.as_view(), name='lantransferinstrument_hr-create'),
    path('lantransferinstrument/<int:pk>/hr_sign_update/', LanTransferInstrumentHRUpdateView.as_view(), name='lantransferinstrument_hr-update'),
    path('lantransferinstrument/<int:pk>/it_sign/', LanTransferInstrumentITCreateView.as_view(), name='lantransferinstrument_it-create'),
    path('lantransferinstrument/<int:pk>/it_sign_update/', LanTransferInstrumentITUpdateView.as_view(), name='lantransferinstrument_it-update'),
    path('lantransferinstrument/<int:pk>/pdf/', LanTransferInstrumentPDF.as_view(), name='lantransferinstrument-pdf'),
    #------------------------------------------------------------------------------------------------------------------------------------

    #---------------------------------------Internet--------------------------------------------------------
    path('internet/<int:pk>/', InternetDetailView.as_view(), name='internet-detail'),

    path('internet/new/', InternetCreateView.as_view(), name='internet-create'),
    path('internet/<int:pk>/update', InternetUpdateView.as_view(), name='internet-update'),

    path('internet/<int:pk>/hod_sign', InternetHODCreateView.as_view(), name='internethod-create'),
    path('internet/<int:pk>/hod_sign_update', InternetHODUpdateView.as_view(), name='internethod-update'),

    path('internet/<int:pk>/hr_sign', InternetHRCreateView.as_view(), name='internethr-create'),
    path('internet/<int:pk>/hr_sign_update', InternetHRUpdateView.as_view(), name='internethr-update'),

    path('internet/<int:pk>/it_sign', InternetITCreateView.as_view(), name='internetit-create'),
    path('internet/<int:pk>/it_sign_update', InternetITUpdateView.as_view(), name='internetit-update'),

    
    path('internet/<int:pk>/pdf', InternetPDF.as_view(), name='internet-pdf'),
    #-------------------------------------------------------------------------------------------------------

    # ---------------------------------------Permission--------------------------------------------------------
    path('permission/<int:pk>/', PermissionDetailView.as_view(), name='permission-detail'),

    path('permission/new/', PermissionCreateView.as_view(), name='permission-create'),
    path('permission/<int:pk>/update', PermissionUpdateView.as_view(), name='permission-update'),

    path('permission/<int:pk>/hod_sign', PermissionHODCreateView.as_view(), name='permissionhod-create'),
    path('permission/<int:pk>/hod_sign_update', PermissionHODUpdateView.as_view(), name='permissionhod-update'),


    path('permission/<int:pk>/hr_sign', PermissionHRCreateView.as_view(), name='permissionhr-create'),
    path('permission/<int:pk>/hr_sign_update', PermissionHRUpdateView.as_view(), name='permissionhr-update'),

    path('permission/<int:pk>/it_sign', PermissionITCreateView.as_view(), name='permissionit-create'),
    path('permission/<int:pk>/it_sign_update', PermissionITUpdateView.as_view(), name='permissionit-update'),
    
    path('permission/<int:pk>/pdf', PermissionPDF.as_view(), name='permission-pdf'),
    # -------------------------------------------------------------------------------------------------------

    # ---------------------------------------File Access-----------------------------------------------------
    path('fileaccess/<int:pk>/', FileAccessDetailView.as_view(), name='file-detail'),

    path('fileaccess/new/', FileAccessCreateView.as_view(), name='file-create'),
    path('fileaccess/<int:pk>/update', FileAccessUpdateView.as_view(), name='file-update'),

    path('fileaccess/<int:pk>/other_hod_sign', FileAccessOtherHODCreateView.as_view(), name='file-otherhod-sign-create'),
    path('fileaccess/<int:pk>/other_hod_sign_update', FileAccessOtherHODUpdateView.as_view(), name='file-otherhod-sign-update'),

    path('fileaccess/<int:pk>/sign', FileAccessSignCreateView.as_view(), name='filesign-create'),
    path('fileaccess/<int:pk>/sign_update', FileAccessSignUpdateView.as_view(), name='filesign-update'),

    path('fileaccess/<int:pk>/hod_sign', FileAccessHODCreateView.as_view(), name='filehod-create'),
    path('fileaccess/<int:pk>/hod_sign_update', FileAccessHODUpdateView.as_view(), name='filehod-update'),

    path('fileaccess/<int:pk>/it_sign', FileAccessITCreateView.as_view(), name='fileit-create'),
    path('fileaccess/<int:pk>/it_sign_update', FileAccessITUpdateView.as_view(), name='fileit-update'),
    
    # path('file_link/<pk>/', FileLinkCreateView.as_view(), name='filelink-create'),
        
    path('file_link/<pk>/', create_filelink, name='filelink-create'),
    # path('file_link/<pk>/', FileLinkCreateView.as_view(), name='filelink-create'),

    path('create_filelink_form/', create_filelink_form, name='create-filelink-form'),
    path('filelink/<pk>/', detail_filelink, name="detail-filelink"),

    # path('filelink/<pk>/update/', FileLinkUpdateView.as_view(), name="update-filelink"),
    # path('filelink/<int:pk>/update/', FileLinkUpdateView.as_view(), name='update-filelink'),
    # path('create-mail-form/', views.create_mail_form, name='create-mail-form'),
    path('filelink/<pk>/update/', update_filelink, name="update-filelink"),

    path('filelink/<pk>/delete/', delete_filelink, name="delete-filelink"),
    path('send_mail/', send_mail, name='send_mail'),


    path('fileaccess/<int:pk>/pdf', FileAccessPDF.as_view(), name='file-pdf'),
    # -------------------------------------------------------------------------------------------------------

    #---------------------------------------display----------------------------------------------------------
    path('display_switch', views.display_switch, name='display_switch'),
    path('display_ip_free', views.display_ip_free, name='display_ip_free'),
    path('display_ip_used', views.display_ip_used, name='display_ip_used'),
    path('display_inventory/', display_inventory, name='display_inventory'),


]
