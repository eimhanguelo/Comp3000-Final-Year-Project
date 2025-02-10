from sre_constants import SUCCESS
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives

from .models import *
from ticket.models import *


from .forms import  *

from django.db.models import Count

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
from django.db.models import Sum
from django.contrib.auth.models import User
import time  # Import the time module
from blog.views import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def display_name_recommender(request):
    try:
        author = request.user 
        if not author.profile.department or not author.profile.location:
            return JsonResponse({"error": "Your profile is missing department or location."}, status=400)

        users = User.objects.filter(
            Q(profile__recom_permission_departments=author.profile.department) & 
            Q(profile__recom_permission_locations=author.profile.location)
        )

        results = [{'id': user.id, 'first_name': user.first_name} for user in users]
        return JsonResponse(results, safe=False)
    
    except AttributeError:
        return HttpResponseForbidden("You are not authorized to access this resource.")

@login_required
def display_name_hod(request):
    try:
        author = request.user  
        if not author.profile.department or not author.profile.location:
            return JsonResponse({"error": "Your profile is missing department or location."}, status=400)

        users = User.objects.filter(
            Q(profile__hod_permission_departments=author.profile.department) & 
            Q(profile__hod_permission_locations=author.profile.location)
        )
        
        results = [{'id': user.id, 'first_name': user.first_name} for user in users]

        return JsonResponse(results, safe=False)
    
    except AttributeError:
        return HttpResponseForbidden("You are not authorized to access this resource.")

def custom_403_view(request, exception=None):
    return render(request, 'connectivity/403.html', status=403)

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

def Req_creation_Acc_mail(raiser, pk, recipient, form_id, link):

    
    Context = {'raiser_name': raiser.first_name,
                'raiser_designation': raiser.profile.position,
                'raiser_dept': raiser.profile.department,
                'raiser_mobile': raiser.profile.phone,
                'raiser_ext': raiser.profile.ext,
                'link': link,
                'id': form_id,
                }

    html_message = render_to_string('blog/e_req_acc_create.html', Context)
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        f"[{form_id}] Asset No Requisition - For Info Only",
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

def req_approved_mail(form_id, link, signer):

    Context = {'author': form_id.author.first_name,
                'form_id': form_id,
                'link': link,
                'signer': signer.first_name,
                }

    html_message = render_to_string('blog/req_approved.html', Context)
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        '[ ' + str(form_id) + ' ] Approved Notification by ' + str(signer),
        plain_message, settings.EMAIL_HOST_USER,
        [form_id.author.email],
        cc=[signer.email]
    )
    msg.attach_alternative(html_message, "text/html")
    msg.send()

def load_models(request):
    product_id = request.GET.get('product')    
    models = ProductModel.objects.filter(product_id=product_id).order_by('name')
    context = {'models': models}
    return render(request, 'hardware/model_dropdown_list_options.html', context)


class RequisitionDetailView(LoginRequiredMixin, DetailView):
    model = Requisition

    def get_context_data(self, **kwargs):

        form_id = self.get_object()      

        context = super().get_context_data(**kwargs)
        requisition = self.object
        context['user_history'] = User.history.filter(
            history_date__lte=requisition.date_updated,
            id=requisition.author.id
        ).values().latest('history_date')
        
        context['profile_history'] = Profile.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.author.profile.id)

        context['recommended_history'] = User.history.filter(
            history_date__lte=requisition.date_updated,
            id=requisition.recommended_by.id
        ).values().latest('history_date')

        context['recommend_hod_history'] = User.history.filter(
            history_date__lte=requisition.date_updated,
            id=requisition.recommended_hod.id
        ).values().latest('history_date')

        context['recommend_hr_history'] = (
            User.history.filter(
                history_date__lte=requisition.date_updated,
                id=requisition.recommended_hr.first().id
            ).values().latest('history_date')
            if requisition.recommended_hr.exists() else 'not_required'
        )

        def get_signer_history(attribute, signer_attribute='signer'):
            related_obj = getattr(requisition, attribute, None)
            if related_obj and signer_attribute:
                signer = getattr(related_obj, signer_attribute, None)
                if signer:
                    return User.history.filter(
                        history_date__lte=requisition.date_updated,
                        id=signer.id
                    ).values().latest('history_date')
            return 'not_signed'

        context['signer_history'] = get_signer_history('requisition_sign')
        context['hod_history'] = get_signer_history('requisition_hod')
        context['asset_history'] = get_signer_history('requisition_asset')
        context['hr_history'] = get_signer_history('requisition_hr')
        context['accountant_history'] = get_signer_history('requisition_accountant')
        context['verifierit_history'] = get_signer_history('requisition_verify')
        context['hodit_history'] = get_signer_history('requisition_hod_it')

        if hasattr(requisition, 'requisition_it'):
            context['admin_history'] = User.history.filter(
                history_date__lte=requisition.requisition_it.date_updated,
                id=requisition.requisition_it.admin.id
            ).values().latest('history_date')
        else:
            context['admin_history'] = 'not_signed'

        context['recommended_hr_users'] = requisition.recommended_hr.filter(profile__is_hr=True)
        context['recommended_accountant_users'] = requisition.recommended_accountant.filter(profile__is_accountant=True)
        context['recommended_verifier_it_users'] = requisition.recommended_verifier_it.filter(profile__is_verifier_it=True)
        context['recommended_hod_it_users'] = requisition.recommended_hod_it.filter(profile__is_hod_it=True)
        context['has_product_with_asset_no'] = requisition.has_product_with_asset_no()
        context['is_recommended_by_hod_same'] = requisition.is_recommended_by_hod_same()
        context['is_HR_Super'] = requisition.is_HR_Super()

        return context
		

class RequisitionCreateView(LoginRequiredMixin, CreateView):
    model = Requisition 
    form_class = RequisitionForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        hr_users = User.objects.filter(profile__is_hr=True)
        form.instance.recommended_hr.set(hr_users)

        accountant_users = User.objects.filter(profile__is_accountant=True)
        form.instance.recommended_accountant.set(accountant_users)

        verifier_it_users = User.objects.filter(profile__is_verifier_it=True)
        form.instance.recommended_verifier_it.set(verifier_it_users)

        hod_it_users = User.objects.filter(profile__is_hod_it=True)
        form.instance.recommended_hod_it.set(hod_it_users)

        return response


def send_email(request, requisition_id):
    if request.method == 'POST':
        requisition = get_object_or_404(Requisition, pk=requisition_id)
        pk = requisition.pk
        has_product_with_asset_no = requisition.has_product_with_asset_no() 

        if requisition.requisition_inventory.exists():
            raiser = requisition.author
            form_id = f'RQSN-{pk}/{raiser.id}/{raiser.profile.emp_id}'
            link = f"{settings.WEB_HOST}/requisition/{pk}/"
            recipient_emails_verify = [user.email for user in requisition.recommended_verifier_it.all()]
            creation_mail(requisition.author, requisition_id, recipient_emails_verify, requisition, link)

            if has_product_with_asset_no:
                recipient_emails = [user.email for user in requisition.recommended_accountant.all()]
                Req_creation_Acc_mail(requisition.author, requisition_id, recipient_emails, requisition, link)

            time.sleep(1)
            return redirect("requisition-detail", pk=pk)
        else:
             return redirect("requisition-detail", pk=pk)
    else:
        return HttpResponseNotAllowed(['POST'])


class RequisitionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Requisition
    form_class = RequisitionForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition = Requisition.objects.get(pk=self.kwargs['pk'])
        if request.user != requisition.author:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        requisition = self.get_object()

        if hasattr(requisition, 'requisition_check'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.author = self.request.user
            response = super().form_valid(form)
            pk = form.instance.pk
            raiser = form.instance.author
            recipient_by = form.cleaned_data['recommended_by']
            recipient_hod = form.cleaned_data['recommended_hod']
            recipient_accountant = form.cleaned_data['recommended_accountant']
            recipient_hr = form.cleaned_data['recommended_hr']
            recipient_verifier_it = form.cleaned_data['recommended_verifier_it']
            recipient_hod_it = form.cleaned_data['recommended_hod_it']
            form_id = f'RQSN-{pk}/{raiser.id}/{raiser.profile.emp_id}'
            link = f"{settings.WEB_HOST}/requisition/{pk}/"

            hr_users = User.objects.filter(profile__is_hr=True)
            form.instance.recommended_hr.set(hr_users)
            accountant_users = User.objects.filter(profile__is_accountant=True)
            form.instance.recommended_accountant.set(accountant_users)
            verifier_it_users = User.objects.filter(profile__is_verifier_it=True)
            form.instance.recommended_verifier_it.set(verifier_it_users)
            hod_it_users = User.objects.filter(profile__is_hod_it=True)
            form.instance.recommended_hod_it.set(hod_it_users)
 
            return response

    def test_func(self):
        requisition = self.get_object()
        return self.request.user == requisition.author

class RequisitionVERIFYCreateView(LoginRequiredMixin, CreateView):
    model = RequisitionVERIFY
    fields = ['sign_type', 'comment', 'verified_by_it']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition = Requisition.objects.get(pk=self.kwargs['pk'])
        if request.user not in requisition.recommended_verifier_it.all():
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        requisition_id = self.kwargs['pk']
        form.instance.requisition_id = requisition_id
        form_id = form.instance.requisition
        signer = self.request.user
        link = f"{settings.WEB_HOST}/requisition/{form.instance.requisition_id}/"

        if form.instance.sign_type == "Agreed":
            recipient_emails = [form_id.recommended_by.email]
            creation_mail(form_id.author, requisition_id, recipient_emails, form_id, link)
            reviewed_mail(form_id, link, signer)
    
        elif form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
            
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('requisition-detail', kwargs={'pk': self.kwargs['pk']})


class RequisitionVERIFYUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RequisitionVERIFY
    fields = ['sign_type', 'comment', 'verified_by_it']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition_vit = self.get_object()
        requisition = requisition_vit.requisition
        if request.user not in requisition.recommended_verifier_it.all():
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        requisition = form.instance.requisition  

        if hasattr(requisition, 'requisition_hod'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')

        response = super().form_valid(form)
        link = f"{settings.WEB_HOST}/requisition/{requisition.id}/"

        if form.instance.sign_type == "Agreed":
            recipient_emails = [requisition.recommended_by.email]
            creation_mail(requisition.author, requisition.id, recipient_emails, requisition, link)
            reviewed_mail(requisition, link, form.instance.signer)
        elif form.instance.sign_type == "Disagreed":
            rejected_mail(requisition, link, form.instance.signer)

        return response

    def test_func(self):
        requisition_vit = self.get_object() 
        return self.request.user == requisition_vit.signer 

    def get_success_url(self):
        requisition = self.get_object().requisition
        return reverse('requisition-detail', kwargs={'pk': requisition.id})


class RequisitionSignCreateView(LoginRequiredMixin, CreateView):
    model = RequisitionSign
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition = Requisition.objects.get(pk=self.kwargs['pk'])
        if request.user != requisition.recommended_by:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.requisition_id = self.kwargs['pk']
        form_id = form.instance.requisition
        signer = self.request.user
        link = f"{settings.WEB_HOST}/requisition/{form.instance.requisition_id}/"
        
        if form.instance.sign_type == "Agreed":
            creation_mail(form_id.author, form.instance.requisition_id, [form_id.recommended_hod.email], form_id, link)
            reviewed_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('requisition-detail', kwargs={'pk': self.kwargs.get('pk')})


class RequisitionSignUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RequisitionSign
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition_sign = self.get_object()  
        requisition = requisition_sign.requisition  
        if request.user != requisition.recommended_by:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_id = self.get_object()

        if hasattr(form_id.requisition, 'requisition_hod'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form_id = form.instance.requisition
            signer = self.request.user
            link = f"{settings.WEB_HOST}/requisition/{form.instance.requisition_id}/"
            
            if form.instance.sign_type == "Agreed":
                creation_mail(form_id.author, form.instance.requisition_id, [form_id.recommended_hod.email], form_id, link)
                reviewed_mail(form_id, link, signer)
            if form.instance.sign_type == "Disagreed":
                rejected_mail(form_id, link, signer)

        return super().form_valid(form)

    def test_func(self):
        requisition = self.get_object()
        if self.request.user == requisition.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('requisition-detail', kwargs={'pk': form_id.requisition.id})


class RequisitionHODCreateView(LoginRequiredMixin, CreateView):
    model = RequisitionHOD
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition = Requisition.objects.get(pk=self.kwargs['pk'])
        if request.user != requisition.recommended_hod:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        requisition_id = self.kwargs['pk']
        form.instance.requisition_id = requisition_id
        requisition = get_object_or_404(Requisition, id=requisition_id)
        has_product_with_asset_no = requisition.has_product_with_asset_no
        signer = self.request.user
        is_hr_super = requisition.is_HR_Super()
        link = f"{settings.WEB_HOST}/requisition/{form.instance.requisition_id}/"
        
        if form.instance.sign_type == "Agreed":
            if has_product_with_asset_no:
                if is_hr_super:
                    recipient_emails = [user.email for user in requisition.recommended_accountant.all()]
                else:  
                    recipient_emails = [user.email for user in requisition.recommended_hr.all()]
            else:
                recipient_emails = [user.email for user in requisition.recommended_verifier_it.all()]

            creation_mail(requisition.author, requisition_id, recipient_emails, requisition, link)
            reviewed_mail(requisition, link, signer)

        elif form.instance.sign_type == "Disagreed":
            rejected_mail(requisition, link, signer)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('requisition-detail', kwargs={'pk': self.kwargs['pk']})


class RequisitionHODUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RequisitionHOD
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition_hod = self.get_object()  
        requisition = requisition_hod.requisition 
        if request.user != requisition.recommended_hod:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_id = self.get_object()

        if hasattr(form_id.requisition, 'requisition_hr') or hasattr(form_id.requisition, 'requisition_hod_it'):
            return HttpResponse('You are not allowed to update as your update time is over!')

        requisition = form.instance.requisition
        signer = self.request.user
        requisition_id = requisition.id
        requisition = get_object_or_404(Requisition, id=requisition_id)
        has_product_with_asset_no = requisition.has_product_with_asset_no  
        is_hr_super = requisition.is_HR_Super() 
        link = f"{settings.WEB_HOST}/requisition/{form.instance.requisition_id}/"

        if form.instance.sign_type == "Agreed":
            if has_product_with_asset_no:
                if is_hr_super:
                    recipient_emails = [user.email for user in requisition.recommended_accountant.all()]
                else:
                    recipient_emails = [user.email for user in requisition.recommended_hr.all()]
            else:
                recipient_emails = [user.email for user in requisition.recommended_verifier_it.all()]
            
            creation_mail(requisition.author, requisition_id, recipient_emails, requisition, link)
            reviewed_mail(requisition, link, signer)

        elif form.instance.sign_type == "Disagreed":
            rejected_mail(requisition, link, signer)

        return super().form_valid(form)

    def test_func(self):
        requisition = self.get_object()
        return self.request.user == requisition.signer

    def get_success_url(self):
        form_id = self.get_object().requisition
        return reverse('requisition-detail', kwargs={'pk': form_id.id})


class RequisitionHRCreateView(LoginRequiredMixin, CreateView):
    model = RequisitionHR
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition = Requisition.objects.get(pk=self.kwargs['pk'])
        if request.user not in requisition.recommended_hr.all():
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        requisition_id = self.kwargs['pk']
        form.instance.requisition_id = requisition_id
        form_id = form.instance.requisition
        signer = self.request.user
        link = f"{settings.WEB_HOST}/requisition/{form.instance.requisition_id}/"

        if form.instance.sign_type == "Agreed":
            recipient_emails = [user.email for user in form_id.recommended_accountant.all()]
            creation_mail(form_id.author, requisition_id, recipient_emails, form_id, link)
            reviewed_mail(form_id, link, signer)
    
        elif form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
            
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('requisition-detail', kwargs={'pk': self.kwargs['pk']})

class RequisitionHRUpdateView(LoginRequiredMixin, UpdateView):
    model = RequisitionHR
    fields = ['sign_type', 'comment']


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition_hr = self.get_object()  # Get the EmployeeSign object
        requisition = requisition_hr.requisition  # Get the associated Employee object
        if request.user not in requisition.recommended_hr.all():
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_id = self.get_object()

        if hasattr(form_id.requisition, 'requisition_hod_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')

        form.instance.signer = self.request.user
        response = super().form_valid(form)
        
        requisition_id = form.instance.requisition_id
        signer = self.request.user
        link = f"{settings.WEB_HOST}/requisition/{form.instance.requisition_id}/"

        
        if form.instance.sign_type == "Agreed":    
            recipient_emails = [user.email for user in form_id.requisition.recommended_accountant.all()]
            creation_mail(form_id.requisition.author, requisition_id, recipient_emails, form_id.requisition, link)
            reviewed_mail(form_id.requisition, link, signer)

        elif form.instance.sign_type == "Disagreed":
            rejected_mail(form_id.requisition, link, signer)

        return response

    def test_func(self):
        requisition = self.get_object()
        return self.request.user == requisition.signer

    def get_success_url(self):
        form_id = self.get_object()
        return reverse('requisition-detail', kwargs={'pk': form_id.requisition.id})


#-------------------------------------Requisition Check----------------------------------------------------

class RequisitionACCCreateView(LoginRequiredMixin, CreateView):
    model = RequisitionACC
    fields = ['sign_type','new_asset_no', 'comment']


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition = Requisition.objects.get(pk=self.kwargs['pk'])
        if request.user not in requisition.recommended_accountant.all():
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        requisition_id = self.kwargs['pk']
        form.instance.requisition_id = requisition_id

        form_id = form.instance.requisition
        signer = self.request.user
        link = f"{settings.WEB_HOST}/requisition/{form.instance.requisition_id}/"

        if form.instance.sign_type == "Agreed":
            recipient_emails = [user.email for user in form_id.recommended_hod_it.all()]
            creation_mail(form_id.author, requisition_id, recipient_emails, form_id, link)
            reviewed_mail(form_id, link, signer)
    
        elif form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
            
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('requisition-detail', kwargs={'pk': self.kwargs['pk']})

class RequisitionACCUpdateView(LoginRequiredMixin, UpdateView):
    model = RequisitionACC
    fields = ['sign_type','new_asset_no', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition_acc = self.get_object()  
        requisition = requisition_acc.requisition  
        if request.user not in requisition.recommended_accountant.all():
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_id = self.get_object()

        if hasattr(form_id.requisition, 'requisition_hod_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')

        form.instance.signer = self.request.user
        response = super().form_valid(form)
        
        requisition_id = form.instance.requisition_id
        signer = self.request.user
        link = f"{settings.WEB_HOST}/requisition/{form.instance.requisition_id}/"
        
        if form.instance.sign_type == "Agreed":    
            recipient_emails = [user.email for user in form_id.requisition.recommended_hod_it.all()]
            creation_mail(form_id.requisition.author, requisition_id, recipient_emails, form_id.requisition, link)
            reviewed_mail(form_id.requisition, link, signer)
        elif form.instance.sign_type == "Disagreed":
            rejected_mail(form_id.requisition, link, signer)

        return response

    def test_func(self):
        requisition = self.get_object()
        return self.request.user == requisition.signer

    def get_success_url(self):
        form_id = self.get_object()
        return reverse('requisition-detail', kwargs={'pk': form_id.requisition.id})


#-------------------------------------Requisition Approved----------------------------------------------------
class RequisitionHODITCreateView(LoginRequiredMixin, CreateView):
    model = RequisitionHODIT
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition = Requisition.objects.get(pk=self.kwargs['pk'])
        if request.user not in requisition.recommended_hod_it.all():
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.requisition_id = self.kwargs['pk']

        form_id = form.instance.requisition
        signer = self.request.user
        link = f"{settings.WEB_HOST}/requisition/{form.instance.requisition_id}/"

        if form.instance.sign_type == "Agreed":
            req_approved_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
            
        #=========================Create TIcket========================================
        # if form.instance.sign_type == "Agreed":
        #     category = ProblemCategory.objects.get(id='5')
        #     t = Eticket(
        #         ticket_raiser=form_id.author,
        #         problem_category=category,
        #         problem_description='Please review the reference form for further action.',
        #         reference_form=form_id,
        #         form_link=link,
        #         created_via='AUTOMATED'
        #     )
        #     t.save()

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('requisition-detail', kwargs={'pk': self.kwargs.get('pk')})


class RequisitionHODITUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RequisitionHODIT
    fields = ['sign_type', 'comment']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        requisition_hit = self.get_object()  
        requisition = requisition_hit.requisition  
        if request.user not in requisition.recommended_hod_it.all():
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_id = self.get_object()

        if hasattr(form_id.requisition, 'requisition_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:

            form_id = form.instance.requisition
            signer = self.request.user

            # link = "{settings.WEB_HOST}/requisition/" + str(form.instance.requisition_id) + "/"
            link = f"{settings.WEB_HOST}/requisition/{form.instance.requisition_id}/"


        if form.instance.sign_type == "Agreed":
            approved_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
            
        #=========================Create TIcket========================================
        # if form.instance.sign_type == "Agreed":
        #     category = ProblemCategory.objects.get(id='5')
        #     t = Eticket(
        #         ticket_raiser=form_id.author,
        #         problem_category=category,
        #         problem_description='Please review the reference form for further action.',
        #         reference_form=form_id,
        #         form_link=link,
        #         created_via='AUTOMATED'
        #     )
        #     t.save()

        return super().form_valid(form)

    def test_func(self):
        requisition = self.get_object()
        if self.request.user == requisition.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('requisition-detail', kwargs={'pk': form_id.requisition.id})


# #-------------------------------------Requisition Check----------------------------------------------------
class RequisitionITCreateView(LoginRequiredMixin, ITUserMixin, CreateView):
    model = RequisitionIT
    fields = ['comment']

    def form_valid(self, form):
        form.instance.admin = self.request.user
        form.instance.requisition_id = self.kwargs['pk']

        form_id = form.instance.requisition
        signer = self.request.user

        # link = "{settings.WEB_HOST}/requisition/" + str(form.instance.requisition_id) + "/"
        link = f"{settings.WEB_HOST}/requisition/{form.instance.requisition_id}/"

        reviewed_mail(form_id, link, signer)

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('requisition-detail', kwargs={'pk': self.kwargs.get('pk')})


class RequisitionITUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = RequisitionIT
    fields = ['comment']

    def form_valid(self, form):
        form_id = self.get_object()       
        form.instance.admin = self.request.user
        form.instance.requisition_id = form_id.requisition.id
        response = super().form_valid(form)
        return response

    def test_func(self):
        requisition = self.get_object()
        if self.request.user == requisition.admin:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('requisition-detail', kwargs={'pk': form_id.requisition.id})

@login_required
def create_prod(request, pk):
    requisition = get_object_or_404(Requisition, pk=pk)
    prods = Inventory.objects.filter(requisition=requisition)
    form = ReqForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            prod = form.save(commit=False)
            prod.requisition = requisition
            prod.creator = request.user
            prod.save()
            return redirect("detail-prod", pk=prod.id)
        else:
            return render(request, "hardware/partials/prod_form.html", {
                "form": form
            })

    context = {
        'form': form,
        'requisition': requisition,
        "prods": prods
    }
    return render(request, 'hardware/prod_create.html', context)
        
        
# @login_required
# def create_prod(request, pk):
#     requisition = Requisition.objects.get(pk=pk)
#     prods = Inventory.objects.filter(requisition=requisition)
#     form = ReqForm(request.POST or None)

#     if request.method == "POST":
#         if form.is_valid():
#             prod = form.save(commit=False)
#             prod.requisition = requisition
#             prod.creator = request.user
#             prod.save()
#             return redirect("detail-prod", pk=prod.id)
#         else:
#             return render(request, "hardware/partials/prod_form.html", {
#                 "form": form
#             })

#     context = {
#         'form': form,
#         'requisition': requisition,
#         "prods": prods
#     }
#     return render(request, 'hardware/prod_create.html', context)


@login_required
def update_prod(request, pk):
    prod = Inventory.objects.get(pk=pk)
    form = ReqForm(request.POST or None, instance=prod)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("detail-prod", pk=prod.id)

    context = {
        "form": form,
        "prod": prod
    }

    return render(request, "hardware/partials/prod_form.html", context)

@login_required
def create_prod_form(request):
    context={
        "form": ReqForm()
    }
    return render(request, "hardware/partials/prod_form.html", context)

@login_required
def detail_prod(request, pk):
    prod = Inventory.objects.get(pk=pk)
    context = {
        "prod": prod
    }
    return render(request, "hardware/partials/prod_detail.html", context)

@login_required
def delete_prod(request, pk):
    prod = Inventory.objects.get(pk=pk)
    prod.delete()
    return HttpResponse('')
    
#---------------------------------------Account PDF------------------------------------
class RequisitionPDF(LoginRequiredMixin, View):
    model = Requisition
    
    def get(self, request, pk, *args, **kwargs):
        
        aa = self.kwargs.get('pk')
        form_id = Requisition.objects.get(pk=aa)
        current_datetime = timezone.now()
       

        data = {
            'runset': form_id,
            'user_history': User.history.filter(history_date__lte=form_id.date_posted, id=form_id.author.id).values().latest(),
            'profile_history': Profile.history.filter(history_date__lte=form_id.date_posted, id=form_id.author.profile.id),
            'current_datetime': current_datetime,  # Adding current date and time
            'printer_by': self.request.user  # Correcting this line by using ':' for dictionary assignment
        }

        #------------------------------------------Signing Portion---------------------------------------
        if hasattr(form_id, 'requisition_sign'): 
            data['signer_history'] = User.history.filter(history_date__lte = form_id.requisition_sign.date_updated,
                                                            id = form_id.requisition_sign.signer.id).values().latest()
        else:
            data['signer_history'] = 'not_signed'

        if hasattr(form_id, 'requisition_hod'): 
            data['hod_history'] = User.history.filter(history_date__lte = form_id.requisition_hod.date_updated,
                                                            id = form_id.requisition_hod.signer.id).values().latest()
        else:
            data['hod_history'] = 'not_signed'


        if hasattr(form_id, 'requisition_asset'):                  
            data['asset_history'] = User.history.filter(history_date__lte = form_id.requisition_asset.date_posted,
                                                            id = form_id.requisition_asset.asset_provider.id).values().latest()
        else:
            data['asset_history'] = 'not_signed'


        if hasattr(form_id, 'requisition_hr'): 
            data['hr_history'] = User.history.filter(history_date__lte = form_id.requisition_hr.date_updated,
                                                            id = form_id.requisition_hr.signer.id).values().latest()
        else:
            data['hr_history'] = 'not_signed'


        if hasattr(form_id, 'requisition_accountant'): 
            data['accountant_history'] = User.history.filter(history_date__lte = form_id.requisition_accountant.date_updated,
                                                            id = form_id.requisition_accountant.signer.id).values().latest()
        else:
            data['accountant_history'] = 'not_signed'


        if hasattr(form_id, 'requisition_verifier_it'):
            data['verifierit_history'] = User.history.filter(history_date__lte = form_id.requisition_verifier_it.date_updated,
                                                            id = form_id.requisition_verifier_it.signer.id).values().latest()
        else:
            data['verifierit_history'] = 'not_signed'

        if hasattr(form_id, 'requisition_hod_it'): 
            data['hodit_history'] = User.history.filter(history_date__lte = form_id.requisition_hod_it.date_updated,
                                                            id = form_id.requisition_hod_it.signer.id).values().latest()
        else:
            data['hodit_history'] = 'not_signed'

        if hasattr(form_id, 'requisition_it'): 
            data['admin_history'] = User.history.filter(history_date__lte = form_id.requisition_it.date_updated,
                                                            id = form_id.requisition_it.admin.id).values().latest()
        else:
            data['admin_history'] = 'not_signed'
            

        pdf = render_to_pdf('hardware/requisition_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


@login_required
def display_requisition(request):

    if request.is_ajax():
        term = request.GET.get('term')
        name_list = Requisition.objects.all().filter(id__icontains=term)
        return_requisition = list(name_list.values())
        return JsonResponse(return_requisition, safe=False)

    return HttpResponse('return_requisition')

class InventoryListView(ITUserMixin, LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):

        context = {            
            'inventory': Inventory.objects.all().order_by('-date_updated'),
            'total_raised': Inventory.objects.filter(product_condition='Requisition Raised').count(),
            'total_chq': Inventory.objects.filter(product_condition='Sent to CHQ').count(),
            'total_added': Inventory.objects.filter(product_condition='In Stock').count(),
            'total_delivered': Inventory.objects.filter(product_condition='Delivered').count(),
        }
        return render(request, 'hardware/inventory_home.html', context)

class InventoryStockView(ITUserMixin, LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):

        context = {            
            'stock_summary':Inventory.objects.filter(product_condition='In Stock')
                                            .values('product__name')
                                            .annotate(total_quantity=Sum('quantity'))
                                            .order_by('-total_quantity')
        }
        return render(request, 'hardware/stock_summary.html', context)


class InventoryDetailView(ITUserMixin, LoginRequiredMixin, DetailView):
    model = Inventory

class InventoryCreateView(ITUserMixin, LoginRequiredMixin, CreateView):
    model = Inventory
    form_class = InventoryForm
    success_url = reverse_lazy('inventory-home')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class InventoryUpdateView(ITUserMixin, LoginRequiredMixin, UpdateView):
    model = Inventory
    form_class = InventoryForm
    success_url = reverse_lazy('inventory-home')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        inventory = self.get_object()
        if self.request.user == inventory.creator:
            return True
        return False


#------------------------CISCO Phone Inventory List ---------------------
class PhoneListView(ITUserMixin, LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):

        context = {            
            'phone': Phone.objects.all().order_by('-date_updated'),
            'total_reserved': Phone.objects.filter(phone_condition='Reserved').count(),
            'total_used': Phone.objects.filter(phone_condition='In Used').count(),
            'total_repair': Phone.objects.filter(phone_condition='Repair').count(),
            'total_decommission': Phone.objects.filter(phone_condition='Decommission').count(),
        }
        return render(request, 'hardware/phone_home.html', context)


class PhoneDetailView(ITUserMixin, LoginRequiredMixin, DetailView):
    model = Phone

    

class PhoneCreateView(ITUserMixin, LoginRequiredMixin, CreateView):
    model = Phone
    form_class = PhoneForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class PhoneUpdateView(ITUserMixin, LoginRequiredMixin, UpdateView):
    model = Phone
    form_class = PhoneForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
