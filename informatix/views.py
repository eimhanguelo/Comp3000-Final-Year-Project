from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,

)

from informatix.models import *


# Create your views here.
class RosterView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):

        context = {
            'rosters': Roster.objects.filter(is_active=True),

        }
        return render(request, 'informatix/rosters.html', context)