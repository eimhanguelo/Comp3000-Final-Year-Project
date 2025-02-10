from django.urls import path, include
from django.conf.urls import url
from .views import *
from . import views

# Import the custom 403 view
from .views import custom_403_view

# Define the handler for 403 errors
handler403 = custom_403_view

urlpatterns = [

    path('', views.HomeView.as_view(), name='front'),
    
    path('admin-dashboard', views.AdminDashboardView.as_view(), name='admin-dashboard'),

    path('home',AdminHomeView.as_view(), name='admin-home'),
    path('admin_it_forms',AdminITFormListView.as_view(), name='admin-it-forms'),

    # path('send-email-to-chq/', SendEmailToCHQView.as_view(), name='send_email_to_chq'),


    path('user/<str:username>/', UserHomeView.as_view(), name='user-home'),
    path('user/<str:username>/it_forms', UserITFormsListView.as_view(), name='user-it-forms'),
    path('user_review/<str:username>/', UserReviewListView.as_view(), name='user-review'),
    path('network', LanListView.as_view(), name='lan-home'),

#---------------------------------------Employee ----------------------------------------------------------------
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='emp-detail'),
    path('employee/new/', EmployeeCreateView.as_view(), name='emp-create'),
    path('employee/<int:pk>/update', EmployeeUpdateView.as_view(), name='emp-update'),   
    path('employee/<int:pk>/pdf', views.EmployeePDF.as_view(), name='emp-pdf'),

    path('employee/<int:pk>/sign', EmployeeSignCreateView.as_view(), name='empsign-create'),
    path('employee/<int:pk>/sign_update', EmployeeSignUpdateView.as_view(), name='empsign-update'),

    path('employee/<int:pk>/hod', EmployeeHODCreateView.as_view(), name='emphod-create'),
    path('employee/<int:pk>/hod_update', EmployeeHODUpdateView.as_view(), name='emphod-update'), 

    path('employee/<int:pk>/hr', EmployeeHRCreateView.as_view(), name='emphr-create'),
    path('employee/<int:pk>/hr_update', EmployeeHRUpdateView.as_view(), name='emphr-update'),   

    path('employee/<int:pk>/it_sign', EmployeeITCreateView.as_view(), name='empit-create'),
    path('employee/<int:pk>/it_sign_update', EmployeeITUpdateView.as_view(), name='empit-update'),

#-------------------------------------------------------------------------------------------------------
    path('account/<int:pk>/', AccountDetailView.as_view(), name='mail-detail'),
    path('account/new/', AccountCreateView.as_view(), name='mail-create'),
    path('account/<int:pk>/update', AccountUpdateView.as_view(), name='mail-update'),
    path('account/<int:pk>/delete', AccountDeleteView.as_view(), name='mail-delete'),
    path('account/<int:pk>/pdf', views.AccountPDF.as_view(), name='mail-pdf'),
    path('account/<int:pk>/pdf_download', views.AccountDownloadPDF.as_view(), name='mail-pdf-download'),

    path('account/<int:pk>/sign', AccountSignCreateView.as_view(), name='mailsign-create'),
    path('account/<int:pk>/sign_update', AccountSignUpdateView.as_view(), name='mailsign-update'),

    path('account/<int:pk>/hod', AccountHODCreateView.as_view(), name='mailhod-create'),
    path('account/<int:pk>/hod_update', AccountHODUpdateView.as_view(), name='mailhod-update'),

    path('account/<int:pk>/hr', AccountHRCreateView.as_view(), name='mailhr-create'),
    path('account/<int:pk>/hr_update', AccountHRUpdateView.as_view(), name='mailhr-update'),


    path('account/<int:pk>/it_sign', AccountITCreateView.as_view(), name='mailit-create'),
    path('account/<int:pk>/it_sign_update', AccountITUpdateView.as_view(), name='mailit-update'),
    
    #-------------------------------------------------------------------------------------------------------
    path('resignation/<int:pk>/', ResignationDetailView.as_view(), name='resignation-detail'),

    path('resignation/new/', ResignationCreateView.as_view(), name='resignation-create'),
    path('resignation/<int:pk>/', ResignationUpdateView.as_view(), name='resignation-update'),

    path('resignation/<int:pk>/data', ResignationDataCreateView.as_view(), name='resignation-data-create'),
    path('resignation/<int:pk>/data_update', ResignationDataUpdateView.as_view(), name='resignation-data-update'),

    path('resignation/<int:pk>/archive', ResignationArchiveCreateView.as_view(), name='resignation-archive-create'),
    path('resignation/<int:pk>/archive_update', ResignationArchiveUpdateView.as_view(), name='resignation-archive-update'),

    path('resignation/<int:pk>/ip', ResignationIPCreateView.as_view(), name='resignation-ip-create'),
    path('resignation/<int:pk>/ip_update', ResignationIPUpdateView.as_view(), name='resignation-ip-update'),

    path('resignation/<int:pk>/phone', ResignationPhoneCreateView.as_view(), name='resignation-phone-create'),
    path('resignation/<int:pk>/phone_update', ResignationPhoneUpdateView.as_view(), name='resignation-phone-update'),

    path('resignation/<int:pk>/printer', ResignationPrinterCreateView.as_view(), name='resignation-printer-create'),
    path('resignation/<int:pk>/printer_update', ResignationPrinterUpdateView.as_view(), name='resignation-printer-update'),

    path('resignation/<int:pk>/scanner', ResignationScannerCreateView.as_view(), name='resignation-scanner-create'),
    path('resignation/<int:pk>/scanner_update', ResignationScannerUpdateView.as_view(), name='resignation-scanner-update'),

    path('resignation/<int:pk>/hod', ResignationHODCreateView.as_view(), name='resignation-hod-create'),
    path('resignation/<int:pk>/hod_update', ResignationHODUpdateView.as_view(), name='resignation-hod-update'),

    path('resignation/<int:pk>/internet', ResignationInternetCreateView.as_view(), name='resignation-internet-create'),
    path('resignation/<int:pk>/internet_update', ResignationInternetUpdateView.as_view(), name='resignation-internet-update'),

    path('resignation/<int:pk>/empower', ResignationEmpowerCreateView.as_view(), name='resignation-empower-create'),
    path('resignation/<int:pk>/empower_update', ResignationEmpowerUpdateView.as_view(), name='resignation-empower-update'),


    path('resignation/<int:pk>/chromeleon', ResignationChromeleonCreateView.as_view(), name='resignation-chromeleon-create'),
    path('resignation/<int:pk>/chromeleon_update', ResignationChromeleonUpdateView.as_view(), name='resignation-chromeleon-update'),

    path('resignation/<int:pk>/eqms', ResignationEqmsCreateView.as_view(), name='resignation-eqms-create'),
    path('resignation/<int:pk>/eqms_update', ResignationEqmsUpdateView.as_view(), name='resignation-eqms-update'),

    path('resignation/<int:pk>/standalone', ResignationStandaloneCreateView.as_view(), name='resignation-standalone-create'),
    path('resignation/<int:pk>/standalone_update', ResignationStandaloneUpdateView.as_view(), name='resignation-standalone-update'),

    path('resignation/<int:pk>/disable', ResignationDisableCreateView.as_view(), name='resignation-disable-create'),
    path('resignation/<int:pk>/disable_update', ResignationDisableUpdateView.as_view(), name='resignation-disable-update'),

    path('resignation/<int:pk>/primary', ResignationPrimaryCreateView.as_view(), name='resignation-primary-create'),
    path('resignation/<int:pk>/primary_update', ResignationPrimaryUpdateView.as_view(), name='resignation-primary-update'),

    path('resignation/<int:pk>/deletion', ResignationDeletionCreateView.as_view(), name='resignation-deletion-create'),
    path('resignation/<int:pk>/deletion_update', ResignationDeletionUpdateView.as_view(), name='resignation-deletion-update'),

    path('resignation/<int:pk>/final', ResignationFinalCreateView.as_view(), name='resignation-final-create'),
    path('resignation/<int:pk>/final', ResignationFinalUpdateView.as_view(), name='resignation-final-update'),

    path('resignation/<int:pk>/pdf', ResignationPDF.as_view(), name='resignation-pdf'),

    path('notification', notifications, name='notification'),

    path('test', test, name='test'),

    path('display_name', views.display_name, name='display_name'),
    path('display_name_hr', views.display_name_hr, name='display_name_hr'),
]
