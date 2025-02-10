from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # ------------------------------------------- All Apps -------------------------------------------------------
    path('', include('blog.urls')),
    path('', include('ticket.urls')),
    path('', include('connectivity.urls')),
    path('', include('hardware.urls')),
    path('', include('productivity.urls')),
    path('', include('informatix.urls')),
    path('', include('users.urls')),
    path('', include('tracker.urls')),  # Tracker app URLs
    path("__debug__/", include("debug_toolbar.urls")),

    # ------------------------------------------- All Apps -------------------------------------------------------

    # path('inbox/notifications/', include('notifications.urls', namespace='all_notification')),

    path("select2/", include("django_select2.urls")),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

