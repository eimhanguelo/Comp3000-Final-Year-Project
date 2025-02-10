from multiprocessing import context
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView
)

from .models import *
from .forms import *

from users.models import *
# Create your views here.

class ProductivityAdminUserMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_productivity_admin:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class AdminSuggestionBoxView(LoginRequiredMixin, ProductivityAdminUserMixin , ListView):

    def get(self, request, *args, **kwargs):

                          
        context = {
            'opportunity_tags': OpportunityTag.objects.all(),
            'total_opportunity_tag': OpportunityTag.objects.all().count(),

            'observation_tags': ObservationTag.objects.all(),
            'total_observation_tag': ObservationTag.objects.all().count(),
        }
        return render(request, 'productivity/admin_suggestion_box.html', context)

class UserSuggestionBoxView(LoginRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
                          
        context = {
            'opportunity_tags': OpportunityTag.objects.filter(author=user),
            'total_opportunity_tag': OpportunityTag.objects.filter(author=user).count(),

            'observation_tags': ObservationTag.objects.filter(author=user),
            'total_observation_tag': ObservationTag.objects.filter(author=user).count(),
        }
        return render(request, 'productivity/user_suggestion_box.html', context)


class OpportunityTagDetailView(LoginRequiredMixin, DetailView):
    model = OpportunityTag

    def get_context_data(self, **kwargs):

        form_id = self.get_object()        
        
        context = super(OpportunityTagDetailView, self).get_context_data(**kwargs)
        context['idea_giver_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.idea_giver.id).values().latest()
        context['profile_history'] = Profile.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.idea_giver.profile.id)

        context['author_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.author.id).values().latest()
        context['supervisor_history'] = User.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.supervisor.id).values().latest()

        if hasattr(form_id, 'opportunity_tag'):                  
            context['admin_history'] = User.history.filter(history_date__lte = form_id.opportunity_tag.date_updated,
                                                            id = form_id.opportunity_tag.admin.id).values().latest()
        else:
            context['admin_history'] = 'not_signed'                           
                                                                                                
        return context

class OpportunityTagCreateView(LoginRequiredMixin, CreateView):
    model = OpportunityTag 
    form_class = OpportunityTagCreationForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response


class OpportunityTagUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = OpportunityTag
    form_class = OpportunityTagCreationForm

    def form_valid(self, form):        
        opportunity_tag = self.get_object()

        if hasattr(opportunity_tag, 'opportunity_tag'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.author = self.request.user
            response = super().form_valid(form)
            return response

    def test_func(self):
        opportunity_tag = self.get_object()
        if self.request.user == opportunity_tag.author:
            return True
        return False

class OpportunityTagAdminCreateView(LoginRequiredMixin, ProductivityAdminUserMixin, CreateView):
    model = OpportunityTagAdmin
    fields = ['status', 'comments']

    def form_valid(self, form):
        form.instance.admin = self.request.user
        form.instance.opportunity_tag_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('opportunity-tag-detail', kwargs={'pk': self.kwargs.get('pk')})

class OpportunityTagAdminUpdateView(LoginRequiredMixin, UserPassesTestMixin, ProductivityAdminUserMixin, UpdateView):
    model = OpportunityTagAdmin
    fields = ['status', 'comments']

    def form_valid(self, form):
        form_id = self.get_object()       
        form.instance.admin = self.request.user
        form.instance.opportunity_tag_id = form_id.opportunity_tag.id
        response = super().form_valid(form)
        return response
            
    def test_func(self):
        opportunity_tag = self.get_object()
        if self.request.user == opportunity_tag.admin:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('observation-tag-detail', kwargs={'pk': form_id.observation_tag.id })

#-----------------------------------------Observation Tag--------------------------------------
class ObservationTagDetailView(LoginRequiredMixin, DetailView):
    model = ObservationTag

    def get_context_data(self, **kwargs):

        form_id = self.get_object()        
        
        context = super(ObservationTagDetailView, self).get_context_data(**kwargs)
        context['author_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.author.id).values().latest()
        context['profile_history'] = Profile.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.author.profile.id)


        if hasattr(form_id, 'observation_tag'):                  
            context['admin_history'] = User.history.filter(history_date__lte = form_id.observation_tag.date_updated,
                                                            id = form_id.observation_tag.admin.id).values().latest()
        else:
            context['admin_history'] = 'not_signed'                           
                                                                                                
        return context

class ObservationTagCreateView(LoginRequiredMixin, CreateView):
    model = ObservationTag
    form_class = ObservationTagCreationForm    

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response

class ObservationTagUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ObservationTag
    form_class = ObservationTagCreationForm

    def form_valid(self, form):        
        observation_tag = self.get_object()

        if hasattr(observation_tag, 'observation_tag'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.author = self.request.user
            response = super().form_valid(form)
            return response

    def test_func(self):
        observation_tag = self.get_object()
        if self.request.user == observation_tag.author:
            return True
        return False


class ObservationTagAdminCreateView(LoginRequiredMixin, ProductivityAdminUserMixin, CreateView):
    model = ObservationTagAdmin
    fields = ['status', 'comments']

    def form_valid(self, form):
        form.instance.admin = self.request.user
        form.instance.observation_tag_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('observation-tag-detail', kwargs={'pk': self.kwargs.get('pk')})

class ObservationTagAdminUpdateView(LoginRequiredMixin, UserPassesTestMixin, ProductivityAdminUserMixin, UpdateView):
    model = ObservationTagAdmin
    fields = ['status', 'comments']

    def form_valid(self, form):
        form_id = self.get_object()       
        form.instance.admin = self.request.user
        form.instance.observation_tag_id = form_id.observation_tag.id
        response = super().form_valid(form)
        return response
            
    def test_func(self):
        observation_tag = self.get_object()
        if self.request.user == observation_tag.admin:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('observation-tag-detail', kwargs={'pk': form_id.observation_tag.id })