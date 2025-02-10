from django.urls import path
from .views import UserListView, UserDetailView, CustomLoginView, autocomplete, SyncLdapUsersView, CustomRegisterView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user_list/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/summary/', UserDetailView.as_view(), name='user-summary'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('sync-ldap-users/', SyncLdapUsersView.as_view(), name='sync-ldap-users'),
    path('register/', CustomRegisterView.as_view(), name='register'),
]

