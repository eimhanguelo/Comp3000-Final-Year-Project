from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    
    path('eticket/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('eticket/new/', TicketCreateView.as_view(), name='ticket-create'),

    path('eticket/<str:username>/', UserTicketListView.as_view(), name='ticket-users'),
    path('engineer/<str:username>/', EngineerTicketListView.as_view(), name='ticket-engineers'),
    path('eticket/<int:pk>/assign', EAssignCreateView.as_view(), name='eassisn-create'),

    # path('eticket/<int:pk>/create', TicketAssignView.as_view(), name='assign-create'),

    path('eticket/<int:pk>/discussion', EDiscussionCreateView.as_view(), name='ediscuss-create'),
    path('eticket/<int:pk>/internal_discuss', EInternalCreateView.as_view(), name='einternal-create'),
    path('eticket/<int:pk>/solve', ESolveCreateView.as_view(), name='esolve-create'),



    path('eticket_pending/', PendingTicketListView.as_view(), name='ticket-pending'),

    path('assign_engineer/<pk>/', assign_engineer, name='assign-engineer'),
    path('assign_form/', assign_form, name='assign-form'),
    path('ticket_assign/<pk>/', detail_assign, name="detail-assign"),
]
