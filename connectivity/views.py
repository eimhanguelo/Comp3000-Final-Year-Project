from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives

from hardware.models import *

from .models import *
from ticket.models import *
from .forms import  *

from users.models import Profile

from django.forms import modelformset_factory, inlineformset_factory
from django.contrib import messages

from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from django.http import JsonResponse

from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.views import View

from blog.views import render_to_pdf, ITUserMixin, HRUserMixin

import os

from django.utils.timezone import make_aware

from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from blog.views import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Custom 403 view function
def custom_403_view(request, exception=None):
    return render(request, 'connectivity/403.html', status=403)

#----------------------- get all data from user first name and return via ajax to dropdown --------------------------
def display_switch(request):
    if request.is_ajax():
        term = request.GET.get('term')
        switch_list = Switch.objects.all().filter(name__icontains=term)
        return_switch_list = list(switch_list.values())
        return JsonResponse(return_switch_list, safe=False)

    return HttpResponse('it sends the switch name data')

#----------------------- get all data from user first name and return via ajax to dropdown --------------------------
def display_ip_free(request):
    if request.is_ajax():
        term = request.GET.get('term')
        ip_list = Lan.objects.all().filter(ip_address__icontains=term, ip_used=False)
        return_ip_list = list(ip_list.values())
        return JsonResponse(return_ip_list, safe=False)

    return HttpResponse('it sends the free IP address list')

def display_ip_used(request):
    if request.is_ajax():
        term = request.GET.get('term')
        ip_list = Lan.objects.all().filter(ip_address__icontains=term, ip_used=True)
        return_ip_list = list(ip_list.values())
        return JsonResponse(return_ip_list, safe=False)

    return HttpResponse('it sends the free IP address list')


def display_inventory(request):
    if request.is_ajax():
        term = request.GET.get('term')
        product_list = Inventory.objects.all().filter(product__icontains=term)
        return_product_list = list(product_list.values())
        return JsonResponse(return_product_list, safe=False)

    return HttpResponse('return_product_list')

#-------------------------------------------------------------------------
def creation_mail(raiser, pk, recipient, form_id, link):

    
    Context = {'raiser_name': raiser.first_name,
                'raiser_designation': raiser.profile.position,
                'raiser_dept': raiser.profile.department,
                'raiser_mobile': raiser.profile.phone,
                'raiser_ext': raiser.profile.ext,
                'link': link,
                'id': form_id,
                }

    html_message = render_to_string('blog/e_send.html', Context)
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        '[ ' + str(form_id) + ' ] Form Review and e-Signature',
        plain_message, settings.EMAIL_HOST_USER,
        recipient,
        cc=[raiser.email]
    )
    msg.attach_alternative(html_message, "text/html")
    msg.send()



def reviewed_mail(form_id, link, signer):

    Context = {'author': form_id.author.first_name,
                'form_id': form_id,
                'link': link,
                'signer': signer.first_name,
                }

    html_message = render_to_string('blog/e_reviewed.html', Context)
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        '[ ' + str(form_id) + ' ] Acceptance Notification by ' + str(signer),
        plain_message, settings.EMAIL_HOST_USER,
        [form_id.author.email],
        cc=[signer.email]
    )
    msg.attach_alternative(html_message, "text/html")
    msg.send()



def rejected_mail(form_id, link, signer):

    Context = {'author': form_id.author.first_name,
                'form_id': form_id,
                'link': link,
                'signer': signer.first_name,
                }

    html_message = render_to_string('blog/e_rejected.html', Context)
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        '[ ' + str(form_id) + ' ] Rejection Notification by ' + str(signer),
        plain_message, settings.EMAIL_HOST_USER,
        [form_id.author.email],
        cc=[signer.email]
    )
    msg.attach_alternative(html_message, "text/html")
    msg.send()

    
def approved_mail(form_id, link, signer):

    Context = {'author': form_id.author.first_name,
                'form_id': form_id,
                'link': link,
                'signer': signer.first_name,
                }

    html_message = render_to_string('blog/e_approved.html', Context)
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        '[ ' + str(form_id) + ' ] Approved Notification by ' + str(signer),
        plain_message, settings.EMAIL_HOST_USER,
        [form_id.author.email],
        cc=[signer.email]
    )
    msg.attach_alternative(html_message, "text/html")
    msg.send()
class LanDetailView(ITUserMixin, LoginRequiredMixin, DetailView):
    model = Lan

class LanCreateView(ITUserMixin, LoginRequiredMixin, CreateView):
    model = Lan
    form_class = LanForm

    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)

class LanUpdateView(ITUserMixin, LoginRequiredMixin, UpdateView):
    model = Lan
    form_class = LanForm

    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)

#---------------------------------Lan Request--------------------------------

class LanRequestDetailView(LoginRequiredMixin, DetailView):
    model = LanRequest

    def get_context_data(self, **kwargs):

        form_id = self.get_object()
        
        context = super(LanRequestDetailView, self).get_context_data(**kwargs)

        
        context['user_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.author.id).values().latest()

        context['profile_history'] = Profile.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.author.profile.id)

        context['approved_hod_history'] = User.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.recommended_hod.id).values().latest()

        if hasattr(form_id, 'lanrequest_sign'):                  
            context['signer_history'] = User.history.filter(history_date__lte = form_id.lanrequest_sign.date_updated,
                                                            id = form_id.lanrequest_sign.signer.id).values().latest()
        else:
            context['signer_history'] = 'not_signed' 

        if hasattr(form_id, 'lanrequest_it'):
            context['lan_history'] = Lan.history.filter(history_date__lte = form_id.lanrequest_it.date_updated,
                                                            id = form_id.lanrequest_it.required_ip_address.id)                  
            context['admin_history'] = User.history.filter(history_date__lte = form_id.lanrequest_it.date_updated,
                                                            id = form_id.lanrequest_it.admin.id).values().latest()
        else:
            context['admin_history'] = 'not_signed'

        # Fetch the eTicket related to the LanInstrument (only fetch if it exists)
        ticket = Eticket.objects.filter(reference_form=form_id).first()
        context['eticket'] = ticket

        # Only format the ticket ID and link if the ticket exists
        if ticket:
            context['formatted_ticket_id'] = f'ETCKT-{ticket.pk}/{ticket.ticket_raiser.id}/{ticket.ticket_raiser.profile.emp_id}'
            context['ticket_link'] = f"{settings.WEB_HOST}/eticket/{ticket.pk}/"
        else:
            context['formatted_ticket_id'] = None
            context['ticket_link'] = None

        return context
                                                                              

class LanRequestCreateView(LoginRequiredMixin, CreateView):
    model = LanRequest
    form_class = LanRequestForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        pk = form.instance.pk

        raiser = form.instance.author
        recipient = form.cleaned_data['recommended_hod']

        # form_id = 'LCRF-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
        form_id = f'LCRF-{pk}/{raiser.id}/{raiser.profile.emp_id}'


        # link = "{settings.WEB_HOST}/lanrequest/" + str(pk) + "/"
        link = f"{settings.WEB_HOST}/lanrequest/{pk}/"


        creation_mail(raiser, pk, [recipient.email], form_id, link)

        return response

class LanRequestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LanRequest
    fields = ['justification','recommended_hod']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        lanrequest = LanRequest.objects.get(pk=self.kwargs['pk'])
        if request.user != lanrequest.author:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):        
        lanrequest = self.get_object()

        if hasattr(lanrequest, 'lanrequest_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.author = self.request.user
            response = super().form_valid(form)

            pk = form.instance.pk
            raiser = form.instance.author
            recipient_hod = form.cleaned_data['recommended_hod']

            form_id = 'LCRF-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
            # link = "{settings.WEB_HOST}/lanrequest/" + str(pk) + "/"
            link = f"{settings.WEB_HOST}/lanrequest/{pk}/"



            if not hasattr(lanrequest, 'lanrequest_sign'):         
                if lanrequest.recommended_hod != recipient_hod:
                    creation_mail(raiser, pk, [recipient_hod.email], form_id, link)
            return response

    def test_func(self):
        lanrequest = self.get_object()
        if self.request.user == lanrequest.author:
            return True
        return False

#---------------------------------------------------------------------------------
class LanRequestSignCreateView(LoginRequiredMixin, CreateView):
    model = LanRequestSign
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        lanrequest_sign = LanRequest.objects.get(pk=self.kwargs['pk'])
        if request.user != lanrequest_sign.recommended_hod:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.lanrequest_id = self.kwargs['pk']

        form_id = form.instance.lanrequest
        signer = self.request.user

        # link = "{settings.WEB_HOST}/lanrequest/" + str(form.instance.lanrequest_id) + "/"
        link = f"{settings.WEB_HOST}/lanrequest/{form.instance.lanrequest_id}/"


        if form.instance.sign_type == "Agreed":
            # reviewed_mail(form_id, link, signer)
            approved_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)


        #=========================Create TIcket========================================
        category = ProblemCategory.objects.get(id='7')
        t = Eticket(
            ticket_raiser=form_id.author,
            problem_category=category,
            problem_description='Please review the reference form for further action.',
            reference_form=form_id,
            form_link=link,
            created_via='AUTOMATED'
        )
        t.save() 
        #==============================================================================

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('lan1-detail', kwargs={'pk': self.kwargs.get('pk')})


class LanRequestSignUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LanRequestSign
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        lanrequest_sign = self.get_object()
        lanrequest = lanrequest_sign.lanrequest
        if request.user != lanrequest.recommended_hod:
            return custom_403_view(request)  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_id = self.get_object()
        if hasattr(form_id.lanrequest, 'lanrequest_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.lanrequest_id = form_id.lanrequest.id
            response = super().form_valid(form)
            return response

    def test_func(self):
        lanrequest = self.get_object()
        if self.request.user == lanrequest.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('lan1-detail', kwargs={'pk': form_id.lanrequest.id })


class LanRequestITCreateView(LoginRequiredMixin, ITUserMixin ,CreateView):
    model = LanRequestIT
    form_class = LanRequestITForm

    def form_valid(self, form):  
        form.instance.admin = self.request.user
        form.instance.lanrequest_id = self.kwargs['pk']

        form_id = form.instance.lanrequest

        it_sign = form.instance.required_ip_address
        it_sign.ip_used = True
        it_sign.used_by = form_id.author
        it_sign.location = form_id.author.profile.location
        it_sign.floor = form_id.author.profile.floor
        it_sign.save()


        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('lan1-detail', kwargs={'pk': self.kwargs.get('pk')})



class LanRequestITUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = LanRequestIT
    form_class = LanRequestITForm

    def form_valid(self, form):
        form_id = self.get_object()       
        form.instance.admin = self.request.user
        form.instance.lanrequest_id = form_id.lanrequest.id


        it_sign = form.instance.required_ip_address
        it_sign.ip_used = True
        it_sign.used_by = form_id.lanrequest.author
        it_sign.location = form_id.lanrequest.author.profile.location
        it_sign.floor = form_id.lanrequest.author.profile.floor
        it_sign.save()

        return super().form_valid(form)
            
    def test_func(self):
        lanrequest = self.get_object()
        if self.request.user == lanrequest.admin:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('lan1-detail', kwargs={'pk': form_id.lanrequest.id })


    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Use the custom 403 view function
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)



#---------------------------------------Lan Request PDF-----------------------------------------
class LanRequestPDF(LoginRequiredMixin, View):
    model = LanRequest
  
    def get(self, request, pk, *args, **kwargs):
        
        aa = self.kwargs.get('pk')
        form_id = LanRequest.objects.get(pk=aa)

        if hasattr(form_id, 'lanrequest_sign'):                  
            signer_history = User.history.filter(history_date__lte = form_id.lanrequest_sign.date_signed,
                                                            id = form_id.lanrequest_sign.signer.id).values().latest()
        else:
            signer_history = 'not_signed' 

        data = {
            'runset': form_id,
            'user_history': User.history.filter(history_date__lte = form_id.date_posted,
                                                id = form_id.author.id).values().latest(),

            'profile_history': Profile.history.filter(history_date__lte = form_id.date_posted, 
                                                            id = form_id.author.profile.id),

            'signer_history': signer_history,


        }
        if hasattr(form_id, 'lanrequest_it'):
            data['lan_history'] = Lan.history.filter(history_date__lte = form_id.lanrequest_it.date_signed,
                                                            id = form_id.lanrequest_it.required_ip_address.id)                  
            data['admin_history'] = User.history.filter(history_date__lte = form_id.lanrequest_it.date_signed,
                                                            id = form_id.lanrequest_it.admin.id).values().latest()
        else:
            data['admin_history'] = 'not_signed'

        pdf = render_to_pdf('connectivity/lanrequest_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


#=============================================Lan Transfer=============================================


class LanTransferDetailView(LoginRequiredMixin, DetailView):
    model = LanTransfer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form_id = self.get_object()
        
        context = super(LanTransferDetailView, self).get_context_data(**kwargs)

        
        context['user_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.author.id).values().latest()

        context['profile_history'] = Profile.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.author.profile.id)

        context['approved_hod_history'] = User.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.recommended_hod.id).values().latest()
        # context['approved_hr_history'] = User.history.filter(history_date__lte = form_id.date_updated,
        #                                                     id = form_id.recommended_hr.all().id).values().latest()
        # Fetch history for each recommended HR user
        if form_id.recommended_hr.exists():
            hr_histories = [
                User.history.filter(
                    history_date__lte=form_id.date_updated,
                    id=hr_user.id
                ).order_by('-history_date').first()
                for hr_user in form_id.recommended_hr.all()
            ]
            context['approved_hr_history'] = hr_histories
        else:
            context['approved_hr_history'] = 'Not Available'



   # Fetch history for the transfer list
        context['all_list'] = [self.get_latest_history(Inventory, o.id, form_id.date_updated) for o in form_id.transfer_list.all()]
    
        if hasattr(form_id, 'lantransfer_hod'):                         
            context['hod_history'] = User.history.filter(history_date__lte = form_id.lantransfer_hod.date_updated,
                                                            id = form_id.lantransfer_hod.signer.id).values().latest()
            context['hod_sign'] = 'yes'
        else:
            context['hod_history'] = 'not_signed'


        if hasattr(form_id, 'lantransfer_hr'):                         
            context['hr_history'] = User.history.filter(history_date__lte = form_id.lantransfer_hr.date_updated,
                                                            id = form_id.lantransfer_hr.signer.id).values().latest()
        else:
            context['hr_history'] = 'not_signed'  

        

        if hasattr(form_id, 'lantransfer_it'):
            context['lan_history'] = Lan.history.filter(history_date__lte = form_id.lantransfer_it.date_updated,
                                                            id = form_id.current_ip_address.id)                           
            context['admin_history'] = User.history.filter(history_date__lte = form_id.lantransfer_it.date_updated,
                                                            id = form_id.lantransfer_it.admin.id).values().latest()
        else:
            context['admin_history'] = 'not_signed'  

        		
		# Fetch the eTicket related to the LanInstrument (only fetch if it exists)
        ticket = Eticket.objects.filter(reference_form=form_id).first()
        context['eticket'] = ticket

        # Only format the ticket ID and link if the ticket exists
        if ticket:
            context['formatted_ticket_id'] = f'ETCKT-{ticket.pk}/{ticket.ticket_raiser.id}/{ticket.ticket_raiser.profile.emp_id}'
            context['ticket_link'] = f"{settings.WEB_HOST}/eticket/{ticket.pk}/"
        else:
            context['formatted_ticket_id'] = None
            context['ticket_link'] = None

        return context


    def get_latest_history(self, model, obj_id, date_updated):
        """Helper method to get the latest history entry."""
        return model.history.filter(history_date__lte=date_updated, id=obj_id).order_by('-history_date').first()


class LanTransferCreateView(LoginRequiredMixin, CreateView):
    model = LanTransfer
    form_class = LanTransferForm


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     response = super().form_valid(form)

    #     hr_users = User.objects.filter(profile__is_hr=True)
    #     form.instance.recommended_hr.set(hr_users)
  
    #     return response


    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        pk = form.instance.pk

        raiser = form.instance.author
        recipient = form.cleaned_data['recommended_hod']

        # form_id = 'LCTF-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)

        form_id = f'LCTF-{pk}/{raiser.id}/{raiser.profile.emp_id}'

        # link = "{settings.WEB_HOST}/lantransfer/" + str(pk) + "/"
        link = f"{settings.WEB_HOST}/lantransfer/{pk}/"



        hr_users = User.objects.filter(profile__is_hr=True)
        form.instance.recommended_hr.set(hr_users)


        creation_mail(raiser, pk, [recipient.email], form_id, link)

        return response

class LanTransferUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LanTransfer
    form_class = LanTransferForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        lantransfer = LanTransfer.objects.get(pk=self.kwargs['pk'])
        if request.user != lantransfer.author:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        lan = self.get_object()

        if hasattr(lan, 'lanrequest_hr'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.author = self.request.user        
            response = super().form_valid(form)

            pk = form.instance.pk
            raiser = form.instance.author
            recipient_hod = form.cleaned_data['recommended_hod']
            # recipient_hr = form.cleaned_data['recommended_hr']

            form_id = 'LCTF-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
            # link = "{settings.WEB_HOST}/lantransfer/" + str(pk) + "/"
            link = f"{settings.WEB_HOST}/lantransfer/{pk}/"


            hr_users = User.objects.filter(profile__is_hr=True)
            form.instance.recommended_hr.set(hr_users)

            creation_mail(raiser, pk, [recipient_hod.email], form_id, link)

            # if not hasattr(lan, 'lantransfer_hod'):         
            #     if lan.recommended_hod != recipient_hod:
            #         creation_mail(raiser, pk, [recipient_hod.email], form_id, link)

            # if hasattr(lan, 'lantransfer_hod') and (not hasattr(lan, 'lantransfer_hr')):  
            #     if lan.recommended_hr != recipient_hr:
            #         creation_mail(raiser, pk, [recipient_hr.email], form_id, link)

            return response

    def test_func(self):
        lan = self.get_object()
        if self.request.user == lan.author:
            return True
        return False

#--------------------------------------------------------------------------------------------
class LanTransferHODCreateView(LoginRequiredMixin, CreateView):
    model = LanTransferHOD
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        lantransfer_hod = LanTransfer.objects.get(pk=self.kwargs['pk'])
        if request.user != lantransfer_hod.recommended_hod:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.lantransfer_id = self.kwargs['pk']

        form_id = form.instance.lantransfer
        signer = self.request.user

        # link = "{settings.WEB_HOST}/lantransfer/" + str(form.instance.lantransfer_id) + "/"
        link = f"{settings.WEB_HOST}/lantransfer/{form.instance.lantransfer_id}/"

        if form.instance.sign_type == "Agreed":
            recipient_emails = [user.email for user in form_id.recommended_hr.all()]
            creation_mail(form_id.author, form.instance.lantransfer_id, recipient_emails, form_id, link)
            reviewed_mail(form_id, link, signer)
    
        elif form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
            
        return super().form_valid(form)

        # recipient = form_id.recommended_hr.email
        # creation_mail(form_id.author, form.instance.lantransfer_id, [recipient], form_id, link)

        # reviewed_mail(form_id, link, signer)

        # return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('lan2-detail', kwargs={'pk': self.kwargs.get('pk')})

class LanTransferHODUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LanTransferHOD
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        lantransfer_hod = self.get_object()
        lantransfer = lantransfer_hod.lantransfer
        if request.user != lantransfer.recommended_hod:
            return custom_403_view(request)  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_id = self.get_object()
        if hasattr(form_id.lantransfer, 'lantransfer_hr'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.lantransfer_id = form_id.lantransfer.id
            form_id = form.instance.lantransfer
            signer = self.request.user

            # link = "{settings.WEB_HOST}/lantransfer/" + str(form.instance.lantransfer_id) + "/"
            link = f"{settings.WEB_HOST}/lantransfer/{form.instance.lantransfer_id}/"


            if form.instance.sign_type == "Agreed":
                recipient_emails = [user.email for user in form_id.recommended_hr.all()]
                creation_mail(form_id.author, form.instance.lantransfer_id, recipient_emails, form_id, link)
                reviewed_mail(form_id, link, signer)
        
            elif form.instance.sign_type == "Disagreed":
                rejected_mail(form_id, link, signer)
                
            return super().form_valid(form)

    def test_func(self):
        lantransfer = self.get_object()
        if self.request.user == lantransfer.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('lan2-detail', kwargs={'pk': form_id.lantransfer.id})


#--------------------------------------------------------------------------------------------
class LanTransferHRCreateView(LoginRequiredMixin, HRUserMixin, CreateView):
    model = LanTransferHR
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        lantransfer_hr = LanTransfer.objects.get(pk=self.kwargs['pk'])
        if request.user not in lantransfer_hr.recommended_hr.all():
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.lantransfer_id = self.kwargs['pk']

        form_id = form.instance.lantransfer
        signer = self.request.user

        # link = "{settings.WEB_HOST}/lantransfer/" + str(form.instance.lantransfer_id) + "/"
        link = f"{settings.WEB_HOST}/lantransfer/{form.instance.lantransfer_id}/"

        if form.instance.sign_type == "Agreed":
            # reviewed_mail(form_id, link, signer)
            approved_mail(form_id, link, signer)
        
        elif form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)

        #=========================Create TIcket========================================
        category = ProblemCategory.objects.get(id='7')
        t = Eticket(
            ticket_raiser=form_id.author,
            problem_category=category,
            problem_description='Please review the reference form for further action.',
            reference_form=form_id,
            form_link=link,
            created_via='AUTOMATED'
        )
        t.save() 

        #==============================================================================

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('lan2-detail', kwargs={'pk': self.kwargs.get('pk')})


class LanTransferHRUpdateView(LoginRequiredMixin, UpdateView):
    model = LanTransferHR
    fields = ['sign_type', 'comment']

    @method_decorator(login_required, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        lantransfer_hr = self.get_object()
        lantransfer = lantransfer_hr.lantransfer
        if request.user not in lantransfer.recommended_hr.all():
            return custom_403_view(request)  # Redirect to custom 403 page
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_id = self.get_object()
        if hasattr(form_id.lantransfer, 'lantransfer_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.lantransfer_id = form_id.lantransfer.id           
            form_id = form.instance.lantransfer
            signer = self.request.user

            # link = "{settings.WEB_HOST}/lantransfer/" + str(form.instance.lantransfer_id) + "/"
            link = f"{settings.WEB_HOST}/lantransfer/{form.instance.lantransfer_id}/"


            if form.instance.sign_type == "Agreed":
                # reviewed_mail(form_id, link, signer)
                approved_mail(form_id, link, signer)
            
            elif form.instance.sign_type == "Disagreed":
                rejected_mail(form_id, link, signer)

            return super().form_valid(form)

    def test_func(self):
        lantransfer = self.get_object()
        if self.request.user == lantransfer.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('lan2-detail', kwargs={'pk': form_id.lantransfer.id})

#-----------------------------------------------------------------------------------------------------

class LanTransferITCreateView(LoginRequiredMixin, CreateView):
    model = LanTransferIT
    fields = ['comment']

    def form_valid(self, form):
        form.instance.admin = self.request.user
        form.instance.lantransfer_id = self.kwargs['pk']

        #=========================Populate Lan Form===================================
        form_id = form.instance.lantransfer
        it_sign = form_id.current_ip_address
        it_sign.location = form_id.new_location
        it_sign.floor = form_id.new_floor
        it_sign.save()
        #==============================================================================

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('lan2-detail', kwargs={'pk': self.kwargs.get('pk')})



class LanTransferITUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = LanTransferIT
    form_class = ['comment']

    def form_valid(self, form):
        form_id = self.get_object()       
        form.instance.admin = self.request.user
        form.instance.lantransfer_id = form_id.lantransfer.id

        #=========================Populate Lan Form===================================
        it_sign = form_id.lantransfer.current_ip_address
        it_sign.location = form_id.lantransfer.location
        it_sign.floor = form_id.lantransfer.floor
        it_sign.save()
        #=========================================================================

        response = super().form_valid(form)
        return response
            
    def test_func(self):
        lantransfer = self.get_object()
        if self.request.user == lantransfer.admin:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('lan2-detail', kwargs={'pk': form_id.lantransfer.id })

    def dispatch(self, request, *args, **kwargs):
            if not self.test_func():
                # Use the custom 403 view function
                return custom_403_view(request)
            return super().dispatch(request, *args, **kwargs)


#---------------------------------------Lan Request PDF-----------------------------------------
class LanTransferPDF(LoginRequiredMixin, View):
    model = LanTransfer


    def get(self, request, pk, *args, **kwargs):
        
        aa = self.kwargs.get('pk')
        form_id = LanTransfer.objects.get(pk=aa)
    
        data = {
            'runset': form_id,
            'user_history': User.history.filter(history_date__lte = form_id.date_posted,
                                                id = form_id.author.id).values().latest(),

            'profile_history': Profile.history.filter(history_date__lte = form_id.date_posted, 
                                                            id = form_id.author.profile.id),

            'previous_lan': Lan.history.filter(history_date__lte = form_id.date_posted,
                                                            id = form_id.current_ip_address.id),
  

        }

        
        if hasattr(form_id, 'lantransfer_hod'):                         
            data['hod_history'] = User.history.filter(history_date__lte = form_id.lantransfer_hod.date_updated,
                                                            id = form_id.lantransfer_hod.signer.id).values().latest()
        else:
            data['hod_history'] = 'not_signed'


        if hasattr(form_id, 'lantransfer_hr'):                         
            data['hr_history'] = User.history.filter(history_date__lte = form_id.lantransfer_hr.date_updated,
                                                            id = form_id.lantransfer_hr.signer.id).values().latest()
        else:
            data['hr_history'] = 'not_signed'  

        if hasattr(form_id, 'lantransfer_it'):
            data['lan_history'] = Lan.history.filter(history_date__lte = form_id.lantransfer_it.date_signed,
                                                            id = form_id.current_ip_address.id)                           
            data['admin_history'] = User.history.filter(history_date__lte = form_id.lantransfer_it.date_signed,
                                                            id = form_id.lantransfer_it.admin.id).values().latest()
        else:
            data['admin_history'] = 'not_signed'
            data['lan_history'] = 'not_signed'

        pdf = render_to_pdf('connectivity/lantransfer_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

#===============================================Lan Instrument========================================

class LanInstrumentDetailView(LoginRequiredMixin, DetailView):
    model = LanInstrument

    def get_context_data(self, **kwargs):
        form_id = self.get_object()
        
        context = super().get_context_data(**kwargs)

        context['user_history'] = User.history.filter(
            history_date__lte=form_id.date_posted,
            id=form_id.author.id
        ).values().latest()

        context['profile_history'] = Profile.history.filter(
            history_date__lte=form_id.date_posted, 
            id=form_id.author.profile.id
        )

        context['approved_hod_history'] = User.history.filter(
            history_date__lte=form_id.date_posted, 
            id=form_id.recommended_hod.id
        ).values().latest()

        if hasattr(form_id, 'laninstrument_sign'):
            context['signer_history'] = User.history.filter(
                history_date__lte=form_id.laninstrument_sign.date_signed,
                id=form_id.laninstrument_sign.signer.id
            ).values().latest()
        else:
            context['signer_history'] = 'not_signed' 

        if hasattr(form_id, 'laninstrument_it'):
            context['lan_history'] = Lan.history.filter(
                history_date__lte=form_id.laninstrument_it.date_signed,
                id=form_id.laninstrument_it.required_ip_address.id
            )                  
            context['admin_history'] = User.history.filter(
                history_date__lte=form_id.laninstrument_it.date_signed,
                id=form_id.laninstrument_it.admin.id
            ).values().latest()
        else:
            context['admin_history'] = 'not_signed'  

        # Fetch the eTicket related to the LanInstrument (only fetch if it exists)
        ticket = Eticket.objects.filter(reference_form=form_id).first()
        context['eticket'] = ticket

        # Only format the ticket ID and link if the ticket exists
        if ticket:
            context['formatted_ticket_id'] = f'ETCKT-{ticket.pk}/{ticket.ticket_raiser.id}/{ticket.ticket_raiser.profile.emp_id}'
            context['ticket_link'] = f"{settings.WEB_HOST}/eticket/{ticket.pk}/"
        else:
            context['formatted_ticket_id'] = None
            context['ticket_link'] = None

        return context


class LanInstrumentCreateView(LoginRequiredMixin, CreateView):
    model = LanInstrument
    form_class = LanInstrumentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        pk = form.instance.pk

        raiser = form.instance.author
        recipient = form.cleaned_data['recommended_hod']

        # form_id = 'RILC-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
        form_id = f'RILC-{pk}/{raiser.id}/{raiser.profile.emp_id}'


        # link = "{settings.WEB_HOST}/laninstrument/" + str(pk) + "/"
        link = f"{settings.WEB_HOST}/laninstrument/{pk}/"

        creation_mail(raiser, pk, [recipient.email], form_id, link)

        return response


class LanInstrumentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LanInstrument
    form_class = LanInstrumentForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        laninstrument = LanInstrument.objects.get(pk=self.kwargs['pk'])
        if request.user != laninstrument.author:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        laninstrument = self.get_object()

        if hasattr(laninstrument, 'laninstrument_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')

        form.instance.author = self.request.user
        response = super().form_valid(form)

        pk = form.instance.pk
        raiser = form.instance.author
        recipient_hod = form.cleaned_data['recommended_hod']

        form_id = f'RILC-{pk}/{raiser.id}/{raiser.profile.emp_id}'
        # link = reverse('laninstrument_detail', args=[pk])
        link = reverse('lan3-detail', args=[pk])


        if not hasattr(laninstrument, 'laninstrument_sign'):
            if laninstrument.recommended_hod != recipient_hod:
                creation_mail(raiser, pk, [recipient_hod.email], form_id, link)

        return response

    def test_func(self):
        laninstrument = self.get_object()
        return self.request.user == laninstrument.author


#---------------------------------------------------------------------------------------------------
from django.db import transaction
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

class LanInstrumentSignCreateView(LoginRequiredMixin, CreateView):
    model = LanInstrumentSign
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        laninstrument_hod = LanInstrument.objects.get(pk=self.kwargs['pk'])
        if request.user != laninstrument_hod.recommended_hod:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        # Set the signer to the current user and assign the LAN instrument ID
        form.instance.signer = self.request.user
        form.instance.laninstrument_id = self.kwargs['pk']  # LAN instrument being signed

        form_id = form.instance.laninstrument
        signer = self.request.user

        # Generate the dynamic link for the LAN instrument, using the correct 'lan3-detail' pattern
        link = self.request.build_absolute_uri(reverse('lan3-detail', kwargs={'pk': form.instance.laninstrument_id}))

        # Send notification emails based on the type of sign action
        if form.instance.sign_type == "Agreed":
            # reviewed_mail(form_id, link, signer)
            approved_mail(form_id, link, signer)
        elif form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)

        # Create the eTicket only when this view is used (i.e., when the form is signed)
        try:
            category = ProblemCategory.objects.get(id='7')  # Ensure the problem category exists
        except ProblemCategory.DoesNotExist:
            form.add_error(None, 'Problem category not found.')
            return self.form_invalid(form)

        # Create the eTicket object
        t = Eticket(
            ticket_raiser=form_id.author,
            problem_category=category,
            problem_description='Please review the reference form for further action.',
            reference_form=form_id,
            form_link=link,
            created_via='AUTOMATED'
        )
        t.save()  # Save the eTicket

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the LAN instrument detail view after form submission
        return reverse('lan3-detail', kwargs={'pk': self.kwargs.get('pk')})



class LanInstrumentSignUpdateView(LoginRequiredMixin, UpdateView):
    model = LanInstrumentSign
    fields = ['sign_type', 'comment']
		
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        laninstrument_hod = self.get_object()
        laninstrument = laninstrument_hod.laninstrument
        if request.user != laninstrument.recommended_hod:
            return custom_403_view(request)  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_id = self.get_object()
        if hasattr(form_id.laninstrument, 'laninstrument_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.laninstrument_id = form_id.laninstrument.id

            
            form_id = form.instance.laninstrument
            signer = self.request.user

            link = f"{settings.WEB_HOST}/laninstrument/{form.instance.laninstrument_id}/"
            
            if form.instance.sign_type == "Agreed":
                # reviewed_mail(form_id, link, signer)
                 approved_mail(form_id, link, signer)
            
            elif form.instance.sign_type == "Disagreed":
                rejected_mail(form_id, link, signer)

            response = super().form_valid(form)
            return response

    def test_func(self):
        laninstrument = self.get_object()
        if self.request.user == laninstrument.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('lan3-detail', kwargs={'pk': form_id.laninstrument.id })


#---------------------------------------------------------------------------------------------------
class LanInstrumentITCreateView(LoginRequiredMixin, CreateView):
    model = LanInstrumentIT
    form_class = LanInstrumentITForm

    def form_valid(self, form):
        form.instance.admin = self.request.user
        form.instance.laninstrument_id = self.kwargs['pk']

        #=========================Populate Lan Form===================================
        form_id = form.instance.laninstrument
        it_sign = form.instance.required_ip_address
        it_sign.ip_used = True
        it_sign.used_by = form_id.author
        it_sign.location = form_id.author.profile.location
        it_sign.floor = form_id.author.profile.floor
        it_sign.instrument_name = form_id.instrument_name
        it_sign.instrument_id = form_id.instrument_id
        it_sign.save()
        #==============================================================================
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('lan3-detail', kwargs={'pk': self.kwargs.get('pk')})


class LanInstrumentITUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = LanInstrumentIT
    form_class = LanInstrumentITForm

    def form_valid(self, form):
        form_id = self.get_object()       
        form.instance.admin = self.request.user
        form.instance.laninstrument_id = form_id.laninstrument.id

        #=========================Populate Lan Form===================================
        it_sign = form.instance.required_ip_address
        it_sign.ip_used = True
        it_sign.used_by = form_id.laninstrument.author
        it_sign.location = form_id.laninstrument.author.profile.location
        it_sign.floor = form_id.laninstrument.author.profile.floor
        it_sign.instrument_name = form_id.laninstrument.instrument_name
        it_sign.instrument_id = form_id.laninstrument.instrument_id
        it_sign.save()
        #==============================================================================

        response = super().form_valid(form)
        return response
            
    def test_func(self):
        laninstrument = self.get_object()
        if self.request.user == laninstrument.admin:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('lan3-detail', kwargs={'pk': form_id.laninstrument.id })


    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Use the custom 403 view function
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)



#---------------------------------------------------------------------------------------------------
class LanInstrumentPDF(LoginRequiredMixin, View):
    model = LanInstrument
    def get(self, request, pk, *args, **kwargs):
        aa = self.kwargs.get('pk')
        form_id = LanInstrument.objects.get(pk=aa)

        if hasattr(form_id, 'laninstrument_sign'):                  
            signer_history = User.history.filter(history_date__lte = form_id.laninstrument_sign.date_signed,
                                                            id = form_id.laninstrument_sign.signer.id).values().latest()
        else:
            signer_history = 'not_signed' 


       
        data = {
            'runset': form_id,
            'user_history': User.history.filter(history_date__lte = form_id.date_posted,
                                                id = form_id.author.id).values().latest(),

            'profile_history': Profile.history.filter(history_date__lte = form_id.date_posted, 
                                                            id = form_id.author.profile.id),

            'signer_history': signer_history,
           

        }

        if hasattr(form_id, 'laninstrument_it'):
            data['lan_history'] = Lan.history.filter(history_date__lte = form_id.laninstrument_it.date_signed,
                                                            id = form_id.laninstrument_it.required_ip_address.id)                  
            data['admin_history'] = User.history.filter(history_date__lte = form_id.laninstrument_it.date_signed,
                                                            id = form_id.laninstrument_it.admin.id).values().latest()
        else:
            data['admin_history'] = 'not_signed'  
                                                                                                  
        pdf = render_to_pdf('connectivity/laninstrument_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

#------------------------------


class LanTransferInstrumentDetailView(LoginRequiredMixin, DetailView):
    model = LanTransferInstrument

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_id = self.get_object()

        # User and Profile history
        context['user_history'] = User.history.filter(
            history_date__lte=form_id.date_updated,
            id=form_id.author.id
        ).order_by('-history_date').first()

        context['profile_history'] = Profile.history.filter(
            history_date__lte=form_id.date_updated,
            id=form_id.author.profile.id
        ).order_by('-history_date').first()

        # Approved HOD history
        if form_id.recommended_hod:
            context['approved_hod_history'] = User.history.filter(
                history_date__lte=form_id.date_updated,
                id=form_id.recommended_hod.id
            ).order_by('-history_date').first()
        else:
            context['approved_hod_history'] = 'Not Available'

        # Approved HR history (handles multiple HR users)
        if form_id.recommended_hr.exists():
            context['approved_hr_history'] = [
                User.history.filter(
                    history_date__lte=form_id.date_updated,
                    id=hr_user.id
                ).order_by('-history_date').first()
                for hr_user in form_id.recommended_hr.all()
            ]
        else:
            context['approved_hr_history'] = 'Not Available'

        # HOD signing history
        if hasattr(form_id, 'lantransfer_hod'):
            context['hod_history'] = User.history.filter(
                history_date__lte=form_id.lantransfer_hod.date_signed,
                id=form_id.lantransfer_hod.signer.id
            ).order_by('-history_date').first()
            context['hod_sign'] = 'yes'
        else:
            context['hod_history'] = 'not_signed'

        # HR signing history
        if hasattr(form_id, 'lantransfer_hr'):
            context['hr_history'] = User.history.filter(
                history_date__lte=form_id.lantransfer_hr.date_signed,
                id=form_id.lantransfer_hr.signer.id
            ).order_by('-history_date').first()
        else:
            context['hr_history'] = 'not_signed'

        # if hasattr(form_id, 'lantransfer_it'):
        #     # Fetch Lan object history
        #     context['lan_history'] = Lan.history.filter(
        #         history_date__lte=form_id.lantransfer_it.date_signed,
        #         id=form_id.current_ip_address.id
        #     ).order_by('-history_date').first()

        #     # Fetch IT admin user history
        #     context['admin_history'] = User.history.filter(
        #         history_date__lte=form_id.lantransfer_it.date_signed,
        #         id=form_id.lantransfer_it.admin.id
        #     ).order_by('-history_date').first()
        # else:
        #     context['admin_history'] = 'not_signed'


        if hasattr(form_id, 'laninstrumenttransfer_it'):
            # context['lan_history'] = Lan.history.filter(history_date__lte = form_id.laninstrumenttransfer_it.date_updated,
            #                                                 id = form_id.laninstrumenttransfer_it.required_ip_address.id)                  
            context['admin_history'] = User.history.filter(history_date__lte = form_id.laninstrumenttransfer_it.date_updated,
                                                            id = form_id.laninstrumenttransfer_it.admin.id).values().latest()
        else:
            context['admin_history'] = 'not_signed'


        # Fetch the eTicket related to the LanInstrument (only fetch if it exists)
        ticket = Eticket.objects.filter(reference_form=form_id).first()
        context['eticket'] = ticket

        # Only format the ticket ID and link if the ticket exists
        if ticket:
            context['formatted_ticket_id'] = f'ETCKT-{ticket.pk}/{ticket.ticket_raiser.id}/{ticket.ticket_raiser.profile.emp_id}'
            context['ticket_link'] = f"{settings.WEB_HOST}/eticket/{ticket.pk}/"
        else:
            context['formatted_ticket_id'] = None
            context['ticket_link'] = None

        return context


class LanTransferInstrumentCreateView(LoginRequiredMixin, CreateView):
    model = LanTransferInstrument
    form_class = LanTransferInstrumentForm


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        pk = form.instance.pk

        raiser = form.instance.author
        recipient = form.cleaned_data['recommended_hod']

        # form_id = 'ILCT-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
        form_id = f'ILCT-{pk}/{raiser.id}/{raiser.profile.emp_id}'

        # link = "{settings.WEB_HOST}/lantransferinstrument/" + str(pk) + "/"
        link = f"{settings.WEB_HOST}/lantransferinstrument/{pk}/"


        hr_users = User.objects.filter(profile__is_hr=True)
        form.instance.recommended_hr.set(hr_users)


        creation_mail(raiser, pk, [recipient.email], form_id, link)

        return response


# class LanTransferInstrumentCreateView(LoginRequiredMixin, CreateView):
#     model = LanTransferInstrument
#     form_class = LanTransferInstrumentForm

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         response = super().form_valid(form)  # Save the instance and get the response

#         # Retrieve the saved instance
#         form.instance.refresh_from_db()  # Ensure the instance is updated with the ID

#         pk = form.instance.pk
#         raiser = form.instance.author
#         recipient_hod = form.cleaned_data.get('recommended_hod')

#         form_id = f'ILCT-{pk}/{raiser.id}/{raiser.profile.emp_id}'
#         link = self.request.build_absolute_uri(reverse('lantransferinstrument-detail', kwargs={'pk': pk}))

#         # Set recommended HR users
#         hr_users = User.objects.filter(profile__is_hr=True)
#         form.instance.recommended_hr.set(hr_users)

#         # Send email to the HOD if recipient_hod is provided
#         if recipient_hod:
#             creation_mail(raiser, pk, [recipient_hod.email], form_id, link)

#         return response


class LanTransferInstrumentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LanTransferInstrument
    form_class = LanTransferInstrumentForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        lantransferinstrument = LanTransferInstrument.objects.get(pk=self.kwargs['pk'])
        if request.user != lantransferinstrument.author:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        lan_transfer = self.get_object()

        if hasattr(lan_transfer, 'lantransfer_hr'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')

        form.instance.author = self.request.user
        response = super().form_valid(form)  # Save the instance and get the response

        # Retrieve the saved instance
        form.instance.refresh_from_db()  # Ensure the instance is updated with the ID

        pk = form.instance.pk
        raiser = form.instance.author
        recipient_hod = form.cleaned_data.get('recommended_hod')

        form_id = f'ILCT-{pk}/{raiser.id}/{raiser.profile.emp_id}'
        link = self.request.build_absolute_uri(reverse('lantransferinstrument-detail', kwargs={'pk': pk}))

        # Set recommended HR users
        hr_users = User.objects.filter(profile__is_hr=True)
        form.instance.recommended_hr.set(hr_users)

        # Send email to the HOD if recipient_hod is provided
        if recipient_hod:
            creation_mail(raiser, pk, [recipient_hod.email], form_id, link)

        return response

    def test_func(self):
        lan_transfer = self.get_object()
        return self.request.user == lan_transfer.author

class LanTransferInstrumentHODCreateView(LoginRequiredMixin, CreateView):
    model = LanTransferInstrumentHOD
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        lantransferinstrument_hod = LanTransferInstrument.objects.get(pk=self.kwargs['pk'])
        if request.user != lantransferinstrument_hod.recommended_hod:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Set the signer to the currently logged-in user
        form.instance.signer = self.request.user
        
        # Correct field reference: set lantransfer (not lantransferinstrument)
        form.instance.lantransfer = LanTransferInstrument.objects.get(pk=self.kwargs['pk'])

        # Capture the instance for email notifications
        form_id = form.instance.lantransfer
        signer = self.request.user

        # Generate dynamic link using reverse instead of hardcoded URL
        link = self.request.build_absolute_uri(
            reverse('lantransferinstrument-detail', kwargs={'pk': form_id.id})
        )

        # Send emails based on the sign_type
        if form.instance.sign_type == "Agreed":
            recipient_emails = [user.email for user in form_id.recommended_hr.all()]
            creation_mail(form_id.author, form_id.id, recipient_emails, form_id, link)
            reviewed_mail(form_id, link, signer)
        elif form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)

        return super().form_valid(form)

    def get_success_url(self):
        # Correct field reference for redirection after successful form submission
        return reverse('lantransferinstrument-detail', kwargs={'pk': self.object.lantransfer.id})


class LanTransferInstrumentHODUpdateView(LoginRequiredMixin, UpdateView):
    model = LanTransferInstrumentHOD
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        lantransferinstrument_hod = self.get_object()
        lantransfer = lantransferinstrument_hod.lantransfer
        if request.user != lantransfer.recommended_hod:
            return custom_403_view(request)  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Get the related LanTransferInstrument instance
        form_id = self.get_object().lantransfer

        # Prevent updates if the form is already processed by HR
        if hasattr(form_id, 'lantransfer_hr'):
            return HttpResponse('You are not allowed to update as your update time is over!')

        # Set the signer and lantransfer to the current instance
        form.instance.signer = self.request.user
        form.instance.lantransfer = form_id
        signer = self.request.user

        # Generate dynamic link using reverse instead of hardcoded URL
        link = self.request.build_absolute_uri(
            reverse('lantransferinstrument-detail', kwargs={'pk': form_id.id})
        )

        # Send emails based on the sign_type
        if form.instance.sign_type == "Agreed":
            recipient_emails = [user.email for user in form_id.recommended_hr.all()]
            creation_mail(form_id.author, form_id.id, recipient_emails, form_id, link)
            reviewed_mail(form_id, link, signer)
        elif form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)

        return super().form_valid(form)

    def test_func(self):
        # Ensure that only the original signer can update the record
        return self.request.user == self.get_object().signer

    def get_success_url(self):
        # Correct field reference for redirection after successful update
        return reverse('lantransferinstrument-detail', kwargs={'pk': self.object.lantransfer.id})


class LanTransferInstrumentHRCreateView(LoginRequiredMixin, HRUserMixin, CreateView):
    model = LanTransferInstrumentHR  # Ensure the correct model is referenced
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        lantransferinstrument_hr = LanTransferInstrument.objects.get(pk=self.kwargs['pk'])
        if request.user not in lantransferinstrument_hr.recommended_hr.all():
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        # Set the signer to the currently logged-in user
        form.instance.signer = self.request.user
        
        # Correct field reference: use the 'lantransfer' field, not 'lantransferinstrument'
        form.instance.lantransfer = LanTransferInstrument.objects.get(pk=self.kwargs['pk'])

        # Capture the lantransfer instance for email notifications and ticket creation
        form_id = form.instance.lantransfer
        signer = self.request.user

        # Generate dynamic link using reverse instead of hardcoded URL
        link = self.request.build_absolute_uri(
            reverse('lantransferinstrument-detail', kwargs={'pk': form_id.id})
        )

        # Send emails based on the sign_type
        if form.instance.sign_type == "Agreed":
            # reviewed_mail(form_id, link, signer)
            approved_mail(form_id, link, signer)
        
        elif form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)

        #=========================Create Ticket========================================
        category = ProblemCategory.objects.get(id='7')


       # Create the eTicket object
        t = Eticket(
            ticket_raiser=form_id.author,
            problem_category=category,
            problem_description='Please review the reference form for further action.',
            reference_form=form_id,
            form_link=link,
            created_via='AUTOMATED'
        )
        t.save()  # Save the eTicket
        # ticket.save()
        #==============================================================================

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        # Redirect to the lantransferinstrument-detail page after a successful submission
        return reverse('lantransferinstrument-detail', kwargs={'pk': self.kwargs.get('pk')})



class LanTransferInstrumentHRUpdateView(LoginRequiredMixin, UpdateView):
    model = LanTransferInstrumentHR  # Ensure the correct model is referenced
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        lantransferinstrument_hr = self.get_object()
        lantransfer = lantransferinstrument_hr.lantransfer
        if request.user not in lantransfer.recommended_hr.all():
            return custom_403_view(request)  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Get the existing LanTransferHR object
        form_id = self.get_object()

        # Check if the transfer process has already moved to IT, preventing further HR updates
        if hasattr(form_id.lantransfer, 'lantransfer_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')

        # Set the signer and lantransfer to the current instance
        form.instance.signer = self.request.user
        form.instance.lantransfer = form_id.lantransfer
        signer = self.request.user

        # Generate dynamic link using reverse instead of hardcoded URL
        link = self.request.build_absolute_uri(
            reverse('lantransferinstrument-detail', kwargs={'pk': form.instance.lantransfer.id})
        )

        # Send emails based on the sign_type
        if form.instance.sign_type == "Agreed":
            # reviewed_mail(form_id.lantransfer, link, signer)
            approved_mail(form_id.lantransfer, link, signer)
        
        elif form.instance.sign_type == "Disagreed":
            rejected_mail(form_id.lantransfer, link, signer)

        return super().form_valid(form)

    def test_func(self):
        # Ensure that only the HR signer who created the record can update it
        return self.request.user == self.get_object().signer

    def get_success_url(self, **kwargs):
        # Redirect to the lantransferinstrument-detail page after a successful update
        return reverse('lantransferinstrument-detail', kwargs={'pk': self.get_object().lantransfer.id})

class LanTransferInstrumentITCreateView(LoginRequiredMixin, CreateView):
    model = LanTransferInstrumentIT
    form_class = LanTransferInstrumentITForm

    def form_valid(self, form):
        # Assign the current user as the admin
        form.instance.admin = self.request.user
        
        # Get the LanTransferInstrument instance using the pk from the URL
        pk = self.kwargs.get('pk')
        form.instance.lantransfer = LanTransferInstrument.objects.get(pk=pk)

        #=========================Populate Lan Form===================================
        form_id = form.instance.lantransfer
        it_sign = form.instance.required_ip_address
        
        # Update the 'required_ip_address' attributes
        it_sign.ip_used = True
        it_sign.used_by = form_id.author
        it_sign.location = form_id.author.profile.location
        it_sign.floor = form_id.author.profile.floor
        
        # Save the changes to the 'required_ip_address' instance
        it_sign.save()
        #==============================================================================
        
        # Save the form and continue with the standard CreateView behavior
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
       return reverse('lantransferinstrument-detail', kwargs={'pk': self.kwargs.get('pk')})



class LanTransferInstrumentITUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = LanTransferInstrumentIT
    form_class = LanTransferInstrumentITForm

    def form_valid(self, form):
        # Get the form instance
        form_id = self.get_object()
        
        # Set admin and lantransfer_id
        form.instance.admin = self.request.user
        form.instance.lantransfer_id = form_id.lantransfer.id

        #=========================Populate Lan Form===================================
        if form_id.lantransfer:
            current_ip_address = form_id.lantransfer.current_ip_address
            if current_ip_address:
                current_ip_address.location = form_id.lantransfer.new_location
                current_ip_address.floor = form_id.lantransfer.new_floor
                current_ip_address.save()
        #==============================================================================

        return super().form_valid(form)
    
    def test_func(self):
        lantransferinstrument = self.get_object()
        return self.request.user == lantransferinstrument.admin

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('lantransferinstrument-detail', kwargs={'pk': form_id.lantransfer.id})

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Use the custom 403 view function
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)


class LanTransferInstrumentPDF(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        form_id = get_object_or_404(LanTransferInstrument, pk=pk)
        
        # Prepare history data
        data = {
            'runset': form_id,
            'user_history': self.get_user_history(form_id.author, form_id.date_posted),
            'profile_history': self.get_profile_history(form_id.author.profile, form_id.date_posted),
            'previous_lan': self.get_lan_history(form_id.current_ip_address, form_id.date_posted),
        }
        
        # Optional: Add conditionals based on the presence of related records
        data['hod_history'] = self.get_history(form_id.lantransfer_hod, 'hod') if hasattr(form_id, 'lantransfer_hod') else 'not_signed'
        data['hr_history'] = self.get_history(form_id.lantransfer_hr, 'hr') if hasattr(form_id, 'lantransfer_hr') else 'not_signed'
        data['_history'] = self.get_lan_history(form_id.current_ip_address, form_id.lantransfer_it.date_signed) if hasattr(form_id, 'lantransfer_it') else 'not_signed'
        data['admin_history'] = self.get_history(form_id.lantransfer_it, 'admin') if hasattr(form_id, 'lantransfer_it') else 'not_signed'
        
        # Render the PDF
        pdf = render_to_pdf('connectivity/lantransferinstrument_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    def get_user_history(self, user, date_posted):
        """Fetch the latest history for a user up to the given date."""
        return User.history.filter(history_date__lte=make_aware(date_posted), id=user.id).order_by('-history_date').first()

    def get_profile_history(self, profile, date_posted):
        """Fetch the latest history for a profile up to the given date."""
        return Profile.history.filter(history_date__lte=make_aware(date_posted), id=profile.id).order_by('-history_date').first()

    def get_lan_history(self, lan, date_posted):
        """Fetch the latest history for a Lan object up to the given date."""
        return Lan.history.filter(history_date__lte=make_aware(date_posted), id=lan.id).order_by('-history_date').first()

    def get_history(self, related_obj, type):
        """Fetch the latest history for related objects (HOD, HR, or Admin)."""
        if type == 'hod':
            return User.history.filter(history_date__lte=make_aware(related_obj.date_updated), id=related_obj.signer.id).order_by('-history_date').first()
        elif type == 'hr':
            return User.history.filter(history_date__lte=make_aware(related_obj.date_updated), id=related_obj.signer.id).order_by('-history_date').first()
        elif type == 'admin':
            return User.history.filter(history_date__lte=make_aware(related_obj.date_signed), id=related_obj.admin.id).order_by('-history_date').first()
        return 'not_signed'

#-------------------------------------------Internet Access Section---------------------------------------------------

class InternetDetailView(LoginRequiredMixin, DetailView):
    model = Internet

    def get_context_data(self, **kwargs):

        form_id = self.get_object()
        
        
        context = super(InternetDetailView, self).get_context_data(**kwargs)
        context['user_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.author.id).values().latest()
        context['profile_history'] = Profile.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.author.profile.id)

        context['approved_hod_history'] = User.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.recommended_hod.id).values().latest()
        context['approved_hr_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.recommended_hr.id).values().latest()

        if hasattr(form_id, 'internet_hod'):                         
            context['hod_history'] = User.history.filter(history_date__lte = form_id.internet_hod.date_updated,
                                                            id = form_id.internet_hod.signer.id).values().latest()
            context['hod_sign'] = 'yes'
        else:
            context['hod_history'] = 'not_signed'


        if hasattr(form_id, 'internet_hr'):                         
            context['hr_history'] = User.history.filter(history_date__lte = form_id.internet_hr.date_updated,
                                                            id = form_id.internet_hr.signer.id).values().latest()
        else:
            context['hr_history'] = 'not_signed'  

        

        if hasattr(form_id, 'internet_it'):                       
            context['admin_history'] = User.history.filter(history_date__lte = form_id.internet_it.date_updated,
                                                            id = form_id.internet_it.admin.id).values().latest()
        else:
            context['admin_history'] = 'not_signed'      
                       
                                                                                                
        return context


class InternetCreateView(LoginRequiredMixin, CreateView):
    model = Internet
    form_class = InternetCreationForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        pk = form.instance.pk
        raiser = form.instance.author
        recipient = form.cleaned_data['recommended_hod']

        form_id = 'IAAF-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
        # link = "{settings.WEB_HOST}/internet/" + str(pk) + "/"
        link = f"{settings.WEB_HOST}/internet/{pk}/"


        creation_mail(raiser, pk, [recipient.email], form_id, link)

        return response

class InternetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Internet
    fields = ['recommended_hod', 'recommended_hr']

    def form_valid(self, form):
        internet = self.get_object()

        if hasattr(internet, 'internet_hr'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:

            form.instance.author = self.request.user            
            response = super().form_valid(form)

            pk = form.instance.pk
            raiser = form.instance.author
            recipient_hod = form.cleaned_data['recommended_hod']
            recipient_hr = form.cleaned_data['recommended_hr']

            form_id = 'IAAF-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
            # link = "{settings.WEB_HOST}/internet/" + str(pk) + "/"
            link = f"{settings.WEB_HOST}/internet/{pk}/"


            if not hasattr(internet, 'internet_hod'):         
                if internet.recommended_hod != recipient_hod:
                    creation_mail(raiser, pk, [recipient_hod.email], form_id, link)

            if hasattr(internet, 'internet_hod') and (not hasattr(internet, 'internet_hr')):  
                if internet.recommended_hr != recipient_hr:
                    creation_mail(raiser, pk, [recipient_hr.email], form_id, link)

            return response

    def test_func(self):
        internet = self.get_object()
        if self.request.user == internet.author:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Use the custom 403 view function
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

#----------------------------------------------------------------------------------------------------
class InternetHODCreateView(LoginRequiredMixin, CreateView):
    model = InternetHOD
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.internet_id = self.kwargs['pk']

        form_id = form.instance.internet
        signer = self.request.user

        # link = "{settings.WEB_HOST}/internet/" + str(form.instance.internet_id) + "/"
        link = f"{settings.WEB_HOST}/internet/{form.instance.internet_id}/"


        
        recipient = form_id.recommended_hr.email
        creation_mail(form_id.author, form.instance.internet_id, [recipient], form_id, link)

        # ---------------------------- Send Reviwed Mail ------------------------------------
        reviewed_mail(form_id, link, signer)

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('internet-detail', kwargs={'pk': self.kwargs.get('pk')})




class InternetHODUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = InternetHOD
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form_id = self.get_object()
        if hasattr(form_id.internet, 'internet_hr'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.internet_id = form_id.internet.id
            response = super().form_valid(form)
            return response

    def test_func(self):
        internet = self.get_object()
        if self.request.user == internet.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('internet-detail', kwargs={'pk': form_id.internet.id})


    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Use the custom 403 view function
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)


#----------------------------------------------------------------------------------------------------
class InternetHRCreateView(LoginRequiredMixin, HRUserMixin, CreateView):
    model = InternetHR
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.internet_id = self.kwargs['pk']

        form_id = form.instance.internet
        signer = self.request.user

        # link = "{settings.WEB_HOST}/internet/" + str(form.instance.internet_id) + "/"
        link = f"{settings.WEB_HOST}/internet/{form.instance.internet_id}/"


        reviewed_mail(form_id, link, signer)

        #=========================Create TIcket========================================
        category = ProblemCategory.objects.get(id='6')
        t = Eticket(ticket_raiser = form_id.author, problem_category = category,
            problem_description='Check the reference Form', reference_form=form_id)

        t.save()
        #==============================================================================

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('internet-detail', kwargs={'pk': self.kwargs.get('pk')})




class InternetHRUpdateView(LoginRequiredMixin, UserPassesTestMixin, HRUserMixin, UpdateView):
    model = InternetHR
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form_id = self.get_object()
        if hasattr(form_id.internet, 'internet_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.internet_id = form_id.internet.id
            response = super().form_valid(form)
            return response


    def test_func(self):
        internet = self.get_object()
        if self.request.user == internet.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('internet-detail', kwargs={'pk': form_id.internet.id})

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Use the custom 403 view function
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)


#------------------------------------------------------------------------------------------------------

class InternetITCreateView(LoginRequiredMixin, CreateView):
    model = InternetIT
    fields = ['comment']

    def form_valid(self, form):
        form.instance.admin = self.request.user
        form.instance.internet_id = self.kwargs['pk']

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('internet-detail', kwargs={'pk': self.kwargs.get('pk')})




class InternetITUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = InternetIT
    fields = ['comment']
    
    def form_valid(self, form):
        form_id = self.get_object()       
        form.instance.admin = self.request.user
        form.instance.internet_id = form_id.internet.id
        response = super().form_valid(form)
        return response
            

    def test_func(self):
        internet = self.get_object()
        if self.request.user == internet.admin:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('internet-detail', kwargs={'pk': form_id.internet.id })

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Use the custom 403 view function
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)




#---------------------------------------Internet PDF------------------------------------
class InternetPDF(LoginRequiredMixin, View):
    model = Internet
    
    def get(self, request, pk, *args, **kwargs):
        
        aa = self.kwargs.get('pk')
        form_id = Internet.objects.get(pk=aa)


        data = {
            'runset': form_id,
            'user_history': User.history.filter(history_date__lte = form_id.date_posted,
                                                id = form_id.author.id).values().latest(),

            'profile_history': Profile.history.filter(history_date__lte = form_id.date_posted, 
                                                            id = form_id.author.profile.id),

        }
        if hasattr(form_id, 'internet_hod'):                         
            data['hod_history'] = User.history.filter(history_date__lte = form_id.internet_hod.date_updated,
                                                            id = form_id.internet_hod.signer.id).values().latest()
        else:
            data['hod_history'] = 'not_signed'

        if hasattr(form_id, 'internet_hr'):                         
            data['hr_history'] = User.history.filter(history_date__lte = form_id.internet_hr.date_updated,
                                                            id = form_id.internet_hr.signer.id).values().latest()
        else:
            data['hr_history'] = 'not_signed'  

        if hasattr(form_id, 'internet_it'):                       
            data['admin_history'] = User.history.filter(history_date__lte = form_id.internet_it.date_updated,
                                                            id = form_id.internet_it.admin.id).values().latest()
        else:
            data['admin_history'] = 'not_signed'  

        pdf = render_to_pdf('connectivity/internet_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


#-------------------------------------------Admisnistration Permission Section---------------------------------------------------

class PermissionDetailView(LoginRequiredMixin, DetailView):
    model = Permission

    def get_context_data(self, **kwargs):

        form_id = self.get_object()
        
        
        context = super(PermissionDetailView, self).get_context_data(**kwargs)
        context['user_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.author.id).values().latest()
        context['profile_history'] = Profile.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.author.profile.id)

        context['approved_hod_history'] = User.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.recommended_hod.id).values().latest()
        context['approved_hr_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.recommended_hr.id).values().latest()
        if hasattr(form_id, 'permission_hod'):                         
            context['hod_history'] = User.history.filter(history_date__lte = form_id.permission_hod.date_updated,
                                                            id = form_id.permission_hod.signer.id).values().latest()
            context['hod_sign'] = 'yes'
        else:
            context['hod_history'] = 'not_signed'


        if hasattr(form_id, 'permission_hr'):                         
            context['hr_history'] = User.history.filter(history_date__lte = form_id.permission_hr.date_updated,
                                                            id = form_id.permission_hr.signer.id).values().latest()
        else:
            context['hr_history'] = 'not_signed'  

        

        if hasattr(form_id, 'permission_it'):                       
            context['admin_history'] = User.history.filter(history_date__lte = form_id.permission_it.date_updated,
                                                            id = form_id.permission_it.admin.id).values().latest()
        else:
            context['admin_history'] = 'not_signed'       
                       
                                                                                                
        return context

class PermissionCreateView(LoginRequiredMixin, CreateView):
    model = Permission
    form_class = PermissionCreationForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        pk = form.instance.pk
        raiser = form.instance.author
        recipient = form.cleaned_data['recommended_hod']

        form_id = 'UAAP-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
        # link = "{settings.WEB_HOST}/permission/" + str(pk) + "/"
        link = f"{settings.WEB_HOST}/permission/{pk}/"


        creation_mail(raiser, pk, [recipient.email], form_id, link)

        return response

class PermissionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Permission
    fields = ['recommended_hod', 'recommended_hr']

    def form_valid(self, form):
        permission = self.get_object()

        if hasattr(permission, 'permission_hr'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:

            form.instance.author = self.request.user            
            response = super().form_valid(form)

            pk = form.instance.pk
            raiser = form.instance.author
            recipient_hod = form.cleaned_data['recommended_hod']
            recipient_hr = form.cleaned_data['recommended_hr']

            form_id = 'UAAP-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
            # link = "{settings.WEB_HOST}/permission/" + str(pk) + "/"
            link = f"{settings.WEB_HOST}/permission/{pk}/"


            if not hasattr(permission, 'permission_hod'):         
                if permission.recommended_hod != recipient_hod:
                    creation_mail(raiser, pk, [recipient_hod.email], form_id, link)

            if hasattr(permission, 'permission_hod') and (not hasattr(permission, 'permission_hr')):  
                if permission.recommended_hr != recipient_hr:
                    creation_mail(raiser, pk, [recipient_hr.email], form_id, link)

            return response

    def test_func(self):
        permission = self.get_object()
        if self.request.user == permission.author:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Use the custom 403 view function
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

class PermissionHODCreateView(LoginRequiredMixin, CreateView):
    model = PermissionHOD
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.permission_id = self.kwargs['pk']

        form_id = form.instance.permission
        signer = self.request.user

        # link = "{settings.WEB_HOST}/permission/" + str(form.instance.permission_id) + "/"
        link = f"{settings.WEB_HOST}/permission/{form.instance.permission_id}/"

        
        recipient = form_id.recommended_hr.email
        creation_mail(form_id.author, form.instance.permission_id, [recipient], form_id, link)

        # ---------------------------- Send Reviwed Mail ------------------------------------
        reviewed_mail(form_id, link, signer)

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('permission-detail', kwargs={'pk': self.kwargs.get('pk')})





class PermissionHODUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PermissionHOD
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form_id = self.get_object()
        if hasattr(form_id.permission, 'permission_hr'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.permission_id = form_id.permission.id
            response = super().form_valid(form)
            return response

    def test_func(self):
        permission = self.get_object()
        if self.request.user == permission.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('permission-detail', kwargs={'pk': form_id.permission.id})
    

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Use the custom 403 view function
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)


#----------------------------------------------------------------------------------------------------
class PermissionHRCreateView(LoginRequiredMixin, HRUserMixin, CreateView):
    model = PermissionHR
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.permission_id = self.kwargs['pk']

        form_id = form.instance.permission
        signer = self.request.user

        # link = "{settings.WEB_HOST}/permission/" + str(form.instance.permission_id) + "/"
        link = f"{settings.WEB_HOST}/permission/{form.instance.permission_id}/"


        reviewed_mail(form_id, link, signer)

        #=========================Create TIcket========================================
        category = ProblemCategory.objects.get(id='3')
        t = Eticket(ticket_raiser = form_id.author, problem_category = category,
            problem_description='Check the reference Form', reference_form=form_id)

        t.save()
        #==============================================================================

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('permission-detail', kwargs={'pk': self.kwargs.get('pk')})





class PermissionHRUpdateView(LoginRequiredMixin, UserPassesTestMixin, HRUserMixin, UpdateView):
    model = PermissionHR
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form_id = self.get_object()
        if hasattr(form_id.permission, 'permission_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.permission_id = form_id.permission.id
            response = super().form_valid(form)
            return response

    def test_func(self):
        permission = self.get_object()
        if self.request.user == permission.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('permission-detail', kwargs={'pk': form_id.permission.id})


    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Use the custom 403 view function
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)


class PermissionITCreateView(LoginRequiredMixin, CreateView):
    model = PermissionIT
    fields = ['comment']

    def form_valid(self, form):
        form.instance.admin = self.request.user
        form.instance.permission_id = self.kwargs['pk']

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('permission-detail', kwargs={'pk': self.kwargs.get('pk')})





class PermissionITUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = PermissionIT
    fields = ['comment']
    
    def form_valid(self, form):
        form_id = self.get_object()       
        form.instance.admin = self.request.user
        form.instance.permission_id = form_id.permission.id
        response = super().form_valid(form)
        return response
            

    def test_func(self):
        Permission = self.get_object()
        if self.request.user == Permission.admin:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('permission-detail', kwargs={'pk': form_id.permission.id })

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Use the custom 403 view function
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)



#---------------------------------------Internet PDF------------------------------------


class PermissionPDF(LoginRequiredMixin, View):
    model = Permission
    
    def get(self, request, pk, *args, **kwargs):
        
        aa = self.kwargs.get('pk')
        form_id = Permission.objects.get(pk=aa)

        data = {
            'runset': form_id,
            'user_history': User.history.filter(history_date__lte = form_id.date_posted,
                                                id = form_id.author.id).values().latest(),

            'profile_history': Profile.history.filter(history_date__lte = form_id.date_posted, 
                                                            id = form_id.author.profile.id)

        }

        if hasattr(form_id, 'permission_hod'):                         
            data['hod_history'] = User.history.filter(history_date__lte = form_id.permission_hod.date_updated,
                                                            id = form_id.permission_hod.signer.id).values().latest()
        else:
            data['hod_history'] = 'not_signed'

        if hasattr(form_id, 'permission_hr'):                         
            data['hr_history'] = User.history.filter(history_date__lte = form_id.permission_hr.date_updated,
                                                            id = form_id.permission_hr.signer.id).values().latest()
        else:
            data['hr_history'] = 'not_signed'  

        if hasattr(form_id, 'permission_it'):                       
            data['admin_history'] = User.history.filter(history_date__lte = form_id.permission_it.date_updated,
                                                            id = form_id.permission_it.admin.id).values().latest()
        else:
            data['admin_history'] = 'not_signed' 

        pdf = render_to_pdf('connectivity/permission_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

#-------------------------------------------File Server Activation Section---------------------------------------------------

class FileAccessDetailView(LoginRequiredMixin, DetailView):
    model = FileAccess

    def get_context_data(self, **kwargs):

        form_id = self.get_object()
        
        
        context = super(FileAccessDetailView, self).get_context_data(**kwargs)
        context['user_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.author.id).values().latest()
        context['profile_history'] = Profile.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.author.profile.id)

        context['recommended_by_history'] = User.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.recommended_by.id).values().latest()
        context['recommended_hod_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.recommended_hod.id).values().latest()


        if form_id.other_dept_head is None:
            context['other_dept_hod'] = 'not_found'
            other_hod = 'not_found'
        else:
            context['other_dept_hod'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.other_dept_head.id).values().latest()

            other_hod = 'found'

        if hasattr(form_id, 'fileaccess_sign'): 
            context['signer_history'] = User.history.filter(history_date__lte = form_id.fileaccess_sign.date_updated,
                                                            id = form_id.fileaccess_sign.signer.id).values().latest()
        else:
            context['signer_history'] = 'not_signed'

        if hasattr(form_id, 'fileaccess_hod'): 
            context['hod_history'] = User.history.filter(history_date__lte = form_id.fileaccess_hod.date_updated,
                                                            id = form_id.fileaccess_hod.signer.id).values().latest()
        else:
            context['hod_history'] = 'not_signed'

        if hasattr(form_id, 'fileaccess_other_hod'):
            context['other_hod_history'] = User.history.filter(history_date__lte = form_id.fileaccess_other_hod.date_updated,
                                                            id = form_id.fileaccess_other_hod.signer.id).values().latest()
        else:
            context['other_hod_history'] = 'not_signed'


        if hasattr(form_id, 'fileaccess_it'):
            context['admin_history'] = User.history.filter(history_date__lte = form_id.fileaccess_it.date_updated,
                                                            id = form_id.fileaccess_it.admin.id).values().latest()
        else:
            context['admin_history'] = 'not_signed'


        location = 'not_created'

        for l in form_id.file_link.all():
                
            if l.location == 'other':
                context['file_location'] = 'other'
                location = 'other'
                break
            else:
                context['file_location'] = 'self'
                location = 'self'
        
        if location == 'not_created' or (other_hod == 'not_found' and location == 'other') or (other_hod == 'found' and location == 'self'):
            context['alarm'] = 'execution_needed'



        		# Fetch the eTicket related to the LanInstrument (only fetch if it exists)
        ticket = Eticket.objects.filter(reference_form=form_id).first()
        context['eticket'] = ticket

        # Only format the ticket ID and link if the ticket exists
        if ticket:
            context['formatted_ticket_id'] = f'ETCKT-{ticket.pk}/{ticket.ticket_raiser.id}/{ticket.ticket_raiser.profile.emp_id}'
            context['ticket_link'] = f"{settings.WEB_HOST}/eticket/{ticket.pk}/"
        else:
            context['formatted_ticket_id'] = None
            context['ticket_link'] = None

        return context


class FileAccessCreateView(LoginRequiredMixin, CreateView):
    model = FileAccess
    form_class = FileAccessForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        pk = form.instance.pk
        raiser = form.instance.author
        recipient = form.cleaned_data['other_dept_head']

        if recipient is None:
            recipient = form.cleaned_data['recommended_by']

        # form_id = 'FSAF-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
        form_id = f'FSAF-{pk}/{raiser.id}/{raiser.profile.emp_id}'

        link = "{settings.WEB_HOST}/fileaccess/" + str(pk) + "/"

        # creation_mail(raiser, pk, [recipient.email], form_id, link)

        return response

# def send_mail(request):
#     if request.method == 'POST':
#         object_to_process = FileAccess.objects.order_by('-pk').first()
#         pk = object_to_process.pk
#         raiser = object_to_process.author
#         recipient = object_to_process.other_dept_head or object_to_process.recommended_by

#         form_id = f'FSAF-{pk}/{raiser.id}/{raiser.profile.emp_id}'
#         link = f'{settings.WEB_HOST}/fileaccess/{pk}/'
            
#             # Send email
#         creation_mail(raiser, pk, [recipient.email], form_id, link)
#         return redirect("file-detail", pk=pk)



import time  # Import the time module

def send_mail(request):
    if request.method == 'POST':
        object_to_process = FileAccess.objects.order_by('-pk').first()
        
        if object_to_process:
            pk = object_to_process.pk
            raiser = object_to_process.author
            recipient = object_to_process.other_dept_head or object_to_process.recommended_by

            form_id = f'FSAF-{pk}/{raiser.id}/{raiser.profile.emp_id}'
            link = f'{settings.WEB_HOST}/fileaccess/{pk}/'

            # Send email
            creation_mail(raiser, pk, [recipient.email], form_id, link)
            
            # Introduce a delay of 1 second (adjust as needed)
            time.sleep(1)
            
            return redirect("file-detail", pk=pk)
        else:
            # Handle case where no FileAccess objects are found
            return HttpResponse("No FileAccess objects found.")
    else:
        # Handle non-POST requests if needed
        return HttpResponseNotAllowed(['POST'])


class FileAccessUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FileAccess
    form_class = FileAccessForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        fileaccess = FileAccess.objects.get(pk=self.kwargs['pk'])
        if request.user != fileaccess.author:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Add custom labels for the fields
        form.fields['revoke_access'].label = 'Revoke Existing Access (If Needed)'
        form.fields['other_dept_head'].label = 'Approved By (Head of other Dept.) [For Cross-Department Access only]'
        form.fields['recommended_by'].label = 'Recommended By'
        form.fields['recommended_hod'].label = 'Approved By (Head of Dept.)'
        return form
    def form_valid(self, form):

        fileaccess = self.get_object()

        if hasattr(fileaccess, 'fileaccess_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')

        else:
            form.instance.author = self.request.user        
            response = super().form_valid(form)

            pk = form.instance.pk
            raiser = form.instance.author
            recipient_other_hod = form.cleaned_data['other_dept_head']
            recipient_by = form.cleaned_data['recommended_by']
            recipient_hod = form.cleaned_data['recommended_hod']

            form_id = 'FSAF-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
            # link = "{settings.WEB_HOST}/fileaccess/" + str(pk) + "/"
            link = f"{settings.WEB_HOST}/fileaccess/{pk}/"


            if recipient_other_hod is None:
                if not hasattr(fileaccess, 'fileaccess_sign'):         
                    if fileaccess.recommended_by != recipient_by:
                        creation_mail(raiser, pk, [recipient_by.email], form_id, link)

                if hasattr(fileaccess, 'fileaccess_sign') and (not hasattr(fileaccess, 'fileaccess_hod')):  
                    if fileaccess.recommended_hod != recipient_hod:
                        creation_mail(raiser, pk, [recipient_hod.email], form_id, link)
            else:
                if not hasattr(fileaccess, 'fileaccess_other_hod'):         
                    if fileaccess.other_dept_head != recipient_other_hod:
                        creation_mail(raiser, pk, [recipient_other_hod.email], form_id, link)

                if hasattr(fileaccess, 'fileaccess_other_hod') and (not hasattr(fileaccess, 'fileaccess_sign')):         
                    if fileaccess.recommended_by != recipient_by:
                        creation_mail(raiser, pk, [recipient_by.email], form_id, link)

                if hasattr(fileaccess, 'fileaccess_sign') and (not hasattr(fileaccess, 'fileaccess_hod')):  
                    if fileaccess.recommended_hod != recipient_hod:
                        creation_mail(raiser, pk, [recipient_hod.email], form_id, link)
            return response
            
    def test_func(self):
        fileaccess = self.get_object()
        if self.request.user == fileaccess.author:
            return True
        return False


# class FileLinkCreateView(LoginRequiredMixin, CreateView):
#     model = FileLink
#     form_class = FileLinkForm
#     template_name = 'connectivity/filelink_create.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         fileaccess = get_object_or_404(FileAccess, pk=self.kwargs['pk'])
#         context['fileaccess'] = fileaccess
#         context['links'] = FileLink.objects.filter(fileaccess=fileaccess)
#         return context

#     def post(self, request, pk):
#         fileaccess = get_object_or_404(FileAccess, pk=pk)
#         links = FileLink.objects.filter(fileaccess=fileaccess)
#         form = FileLinkForm(request.POST)

#         if form.is_valid():
#             link = form.save(commit=False)
#             link.fileaccess = fileaccess
#             link.save()
#             # recipient = fileaccess.other_dept_head or fileaccess.recommended_by
#             # if recipient:
#             #     form_id = f'FSAF-{fileaccess.pk}/{fileaccess.author.id}/{fileaccess.author.profile.emp_id}'
#             #     link_url = f"{settings.WEB_HOST}/fileaccess/{fileaccess.pk}/"
#             #     creation_mail(fileaccess.author, fileaccess.pk, [recipient.email], form_id, link_url)
#             return redirect("detail-filelink", pk=link.id)

#         context = {
#             'form': form,
#             'fileaccess': fileaccess,
#             'links': links
#         }
#         return render(request, 'connectivity/filelink_create.html', context)

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         response = super().form_valid(form)

#         pk = form.instance.pk
#         raiser = form.instance.author
#         recipient = form.cleaned_data['other_dept_head']

#         if recipient is None:
#             recipient = form.cleaned_data['recommended_by']

#         form_id = 'FSAF-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
#         # link = "{settings.WEB_HOST}/fileaccess/" + str(pk) + "/"
#         link = f"{settings.WEB_HOST}/fileaccess/{pk}/"


#         creation_mail(raiser, pk, [recipient.email], form_id, link)

#         return response


# class FileLinkUpdateView(LoginRequiredMixin, UpdateView):
#     def get(self, request, pk):
#         link = FileLink.objects.get(pk=pk)
#         form = FileLinkForm(instance=link)
#         context = {
#             "form": form,
#             "link": link
#         }
#         return render(request, "connectivity/partials/file_form.html", context)

#     def post(self, request, pk):
#         link = FileLink.objects.get(pk=pk)
#         form = FileLinkForm(request.POST, instance=link)
#         if form.is_valid():
#             form.save()
#             return redirect("detail-filelink", pk=link.id)
#         context = {
#             "form": form,
#             "link": link
#         }
#         return render(request, "connectivity/partials/file_form.html", context)

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         response = super().form_valid(form)

#         pk = form.instance.pk
#         raiser = form.instance.author
#         recipient = form.cleaned_data['other_dept_head']

#         if recipient is None:
#             recipient = form.cleaned_data['recommended_by']

#         form_id = 'FSAF-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
#         # link = "{settings.WEB_HOST}/fileaccess/" + str(pk) + "/"
#         link = f"{settings.WEB_HOST}/fileaccess/{pk}/"


#         creation_mail(raiser, pk, [recipient.email], form_id, link)

#         return response

#     def dispatch(self, request, *args, **kwargs):
#         if not self.test_func():
#             # Use the custom 403 view function
#             return custom_403_view(request)
#         return super().dispatch(request, *args, **kwargs)

# class FileLinkUpdateView(LoginRequiredMixin, UpdateView):
#     model = FileLink  
#     form_class = FileLinkForm  # The form used for updating
#     template_name = "connectivity/partials/file_form.html"  
#     success_url = reverse_lazy("filelink-list")  

#     def form_valid(self, form):
#         messages.success(self.request, "FileLink updated successfully!")
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         messages.error(self.request, "There was an error updating the FileLink.")
#         return super().form_invalid(form)

#     def get_object(self, queryset=None):
#         return get_object_or_404(FileLink, pk=self.kwargs["pk"])
@login_required
def create_filelink(request, pk):
    fileaccess = FileAccess.objects.get(pk=pk)
    links = FileLink.objects.filter(fileaccess=fileaccess)
    form = FileLinkForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            link = form.save(commit=False)
            link.fileaccess = fileaccess
            link.save()
            return redirect("detail-filelink", pk=link.id)
        else:
            return render(request, "connectivity/partials/file_form.html", context={
                "form": form
            })

    context = {
        'form': form,
        'fileaccess': fileaccess,
        "links": links
    }
    return render(request, 'connectivity/filelink_create.html', context)

@login_required
def update_filelink(request, pk):
    link = FileLink.objects.get(pk=pk)
    form = FileLinkForm(request.POST or None, instance=link)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("detail-filelink", pk=link.id)

    context = {
        "form": form,
        "link": link
    }

    return render(request, "connectivity/partials/file_form.html", context)

@login_required
def create_filelink_form(request):
    context={
        "form": FileLinkForm()
    }
    return render(request, "connectivity/partials/file_form.html", context)

@login_required
def detail_filelink(request, pk):
    # Retrieve the link object
    link = get_object_or_404(FileLink, pk=pk)

    context = {
        "link": link,
    }

    # Render the template with the context
    return render(request, "connectivity/partials/file_detail.html", context)

@login_required
def delete_filelink(request, pk):
    link = FileLink.objects.get(pk=pk)
    link.delete()
    return HttpResponse('')


#--------------------------------------------------------------------------------------------------
class FileAccessOtherHODCreateView(LoginRequiredMixin, CreateView):
    model = FileAccessOtherHOD
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        fileaccess = FileAccess.objects.get(pk=self.kwargs['pk'])
        if request.user != fileaccess.other_dept_head:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.fileaccess_id = self.kwargs['pk']

        form_id = form.instance.fileaccess
        signer = self.request.user

        # link = "{settings.WEB_HOST}/fileaccess/" + str(form.instance.fileaccess_id) + "/"
        
        
        # recipient = form_id.recommended_by.email
        # creation_mail(form_id.author, form.instance.fileaccess_id, [recipient], form_id, link)

        # # ---------------------------- Send Reviwed Mail ------------------------------------
        # reviewed_mail(form_id, link, signer)


        link = f"{settings.WEB_HOST}/fileaccess/{form.instance.fileaccess_id}/"

        if form.instance.sign_type == "Agreed":
           reviewed_mail(form_id, link, signer)
           recipient = form_id.recommended_by.email
           creation_mail(form_id.author, form.instance.fileaccess_id, [recipient], form_id, link)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('file-detail', kwargs={'pk': self.kwargs.get('pk')})




class FileAccessOtherHODUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FileAccessOtherHOD
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        fileaccess_other_hod = self.get_object()
        fileaccess = fileaccess_other_hod.fileaccess
        if request.user != fileaccess.other_dept_head:
            return custom_403_view(request)  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_id = self.get_object()
        if hasattr(form_id.fileaccess, 'fileaccess_sign'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        # else:
        #     form.instance.signer = self.request.user
        #     form.instance.fileaccess_id = form_id.fileaccess.id
        #     response = super().form_valid(form)
        #     return response

        form_id = form.instance.fileaccess
        signer = self.request.user


        link = f"{settings.WEB_HOST}/fileaccess/{form.instance.fileaccess_id}/"

        if form.instance.sign_type == "Agreed":
            reviewed_mail(form_id, link, signer)
            recipient = form_id.recommended_by.email
            creation_mail(form_id.author, form.instance.fileaccess_id, [recipient], form_id, link)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
        
        return super().form_valid(form)


    def test_func(self):
        fileaccess = self.get_object()
        if self.request.user == fileaccess.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('file-detail', kwargs={'pk': form_id.fileaccess.id})



#--------------------------------------------------------------------------------------------------
class FileAccessSignCreateView(LoginRequiredMixin, CreateView):
    model = FileAccessSign
    fields = ['sign_type', 'comment']


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        fileaccess = FileAccess.objects.get(pk=self.kwargs['pk'])
        if request.user != fileaccess.recommended_by:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.fileaccess_id = self.kwargs['pk']

        form_id = form.instance.fileaccess
        signer = self.request.user

        # link = "{settings.WEB_HOST}/fileaccess/" + str(form.instance.fileaccess_id) + "/"
        
        # recipient = form_id.recommended_hod.email
        # creation_mail(form_id.author, form.instance.fileaccess_id, [recipient], form_id, link)

        # # ---------------------------- Send Reviwed Mail ------------------------------------
        # reviewed_mail(form_id, link, signer)

        link = f"{settings.WEB_HOST}/fileaccess/{form.instance.fileaccess_id}/"

        if form.instance.sign_type == "Agreed":
            reviewed_mail(form_id, link, signer)
            recipient = form_id.recommended_hod.email
            creation_mail(form_id.author, form.instance.fileaccess_id, [recipient], form_id, link)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
        
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('file-detail', kwargs={'pk': self.kwargs.get('pk')})


class FileAccessSignUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FileAccessSign
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        fileaccess_sign = self.get_object()
        fileaccess = fileaccess_sign.fileaccess
        if request.user != fileaccess.recommended_by:
            return custom_403_view(request)  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_id = self.get_object()
        if hasattr(form_id.fileaccess, 'fileaccess_hod'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        # else:
        #     form.instance.signer = self.request.user
        #     form.instance.fileaccess_id = form_id.fileaccess.id
        #     response = super().form_valid(form)
        #     return response
        
        form_id = form.instance.fileaccess
        signer = self.request.user


        link = f"{settings.WEB_HOST}/fileaccess/{form.instance.fileaccess_id}/"

        if form.instance.sign_type == "Agreed":
            reviewed_mail(form_id, link, signer)
            recipient = form_id.recommended_hod.email
            creation_mail(form_id.author, form.instance.fileaccess_id, [recipient], form_id, link)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
        
        return super().form_valid(form)

    def test_func(self):
        fileaccess = self.get_object()
        if self.request.user == fileaccess.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('file-detail', kwargs={'pk': form_id.fileaccess.id})


#--------------------------------------------------------------------------------------------------
class FileAccessHODCreateView(LoginRequiredMixin, CreateView):
    model = FileAccessHOD
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        fileaccess = FileAccess.objects.get(pk=self.kwargs['pk'])
        if request.user != fileaccess.recommended_hod:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.fileaccess_id = self.kwargs['pk']

        form_id = form.instance.fileaccess
        signer = self.request.user

        link = f"{settings.WEB_HOST}/fileaccess/{form.instance.fileaccess_id}/"

        if form.instance.sign_type == "Agreed":
            approved_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
            
        #=========================Create TIcket========================================
        if form.instance.sign_type == "Agreed":
            category = ProblemCategory.objects.get(id='3')
            t = Eticket(
                ticket_raiser=form_id.author,
                problem_category=category,
                problem_description='Please review the reference form for further action.',
                reference_form=form_id,
                form_link=link,
                created_via='AUTOMATED'
            )
            t.save()
        #==============================================================================

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('file-detail', kwargs={'pk': self.kwargs.get('pk')})


class FileAccessHODUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FileAccessHOD
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        fileaccess_hod = self.get_object()
        fileaccess = fileaccess_hod.fileaccess
        if request.user != fileaccess.recommended_hod:
            return custom_403_view(request)  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_id = self.get_object()
        if hasattr(form_id.fileaccess, 'fileaccess_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        form_id = form.instance.fileaccess
        signer = self.request.user

        link = f"{settings.WEB_HOST}/fileaccess/{form.instance.fileaccess_id}/"

        if form.instance.sign_type == "Agreed":
            approved_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
            
        #=========================Create TIcket========================================
        if form.instance.sign_type == "Agreed":
            category = ProblemCategory.objects.get(id='3')
            t = Eticket(
                ticket_raiser=form_id.author,
                problem_category=category,
                problem_description='Please review the reference form for further action.',
                reference_form=form_id,
                form_link=link,
                created_via='AUTOMATED'
            )
            t.save()
        #==============================================================================
        return super().form_valid(form)

    def test_func(self):
        fileaccess = self.get_object()
        if self.request.user == fileaccess.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('file-detail', kwargs={'pk': form_id.fileaccess.id})


#--------------------------------------------------------------------------------------------------


class FileAccessITCreateView(LoginRequiredMixin, ITUserMixin, CreateView):
    model = FileAccessIT
    fields = ['comment']

    def form_valid(self, form):
        form.instance.admin = self.request.user
        form.instance.fileaccess_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('file-detail', kwargs={'pk': self.kwargs.get('pk')})



class FileAccessITUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = FileAccessHOD
    fields = ['comment']
    
    def form_valid(self, form):
        form_id = self.get_object()       
        form.instance.admin = self.request.user
        form.instance.fileaccess_id = form_id.fileaccess.id
        response = super().form_valid(form)
        return response
            

    def test_func(self):
        fileaccess = self.get_object()
        if self.request.user == fileaccess.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('file-detail', kwargs={'pk': form_id.fileaccess.id})

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Use the custom 403 view function
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)


#--------------------------------------------------------------------------------------------------

class FileAccessPDF(LoginRequiredMixin, View):
    model = FileAccess
    
    def get(self, request, pk, *args, **kwargs):
        
        aa = self.kwargs.get('pk')
        form_id = FileAccess.objects.get(pk=aa)

        data = {
            'runset': form_id,
            'user_history': User.history.filter(history_date__lte = form_id.date_posted,
                                                id = form_id.author.id).values().latest(),

            'profile_history': Profile.history.filter(history_date__lte = form_id.date_posted, 
                                                            id = form_id.author.profile.id),
        }

        if hasattr(form_id, 'fileaccess_sign'): 
            data['signer_history'] = User.history.filter(history_date__lte = form_id.fileaccess_sign.date_updated,
                                                            id = form_id.fileaccess_sign.signer.id).values().latest()
        else:
            data['signer_history'] = 'not_signed'

        if hasattr(form_id, 'fileaccess_hod'): 
            data['hod_history'] = User.history.filter(history_date__lte = form_id.fileaccess_hod.date_updated,
                                                            id = form_id.fileaccess_hod.signer.id).values().latest()
        else:
            data['hod_history'] = 'not_signed'

        if hasattr(form_id, 'fileaccess_other_hod'):
            data['other_hod_history'] = User.history.filter(history_date__lte = form_id.fileaccess_other_hod.date_updated,
                                                            id = form_id.fileaccess_other_hod.signer.id).values().latest()
        else:
            data['other_hod_history'] = 'not_signed'


        if hasattr(form_id, 'fileaccess_it'):
            data['admin_history'] = User.history.filter(history_date__lte = form_id.fileaccess_it.date_updated,
                                                            id = form_id.fileaccess_it.admin.id).values().latest()
        else:
            data['admin_history'] = 'not_signed'

        pdf = render_to_pdf('connectivity/fileaccess_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
