from django.urls import path, include
from django.conf.urls import url
from .views import *
from . import views

from informatix.views import *


urlpatterns = [
    path('rosters', RosterView.as_view(), name='roster-home'),

]
