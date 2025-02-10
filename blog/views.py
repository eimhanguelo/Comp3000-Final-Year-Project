from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,

)
from .models import *
from users.models import *
from ticket.models import *
from connectivity.models import *
from hardware.models import *
from informatix.models import *
from .forms import *
from django.db.models import Q
from notifications.signals import notify
import json
from django.http import JsonResponse
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from django.conf import settings
#-------------------------------------------
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from users.views import *

from django.views.generic import TemplateView

class AdminDashboardView(TemplateView):
    template_name = 'blog/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_users': User.objects.count(),  # Total users
            'total_users_staff': User.objects.filter(is_staff=True).count(),  # Staff users
            'total_users_super': User.objects.filter(is_superuser=True).count(),  # Superusers

            'total_tickets': Eticket.objects.count(),  # Total tickets
            'total_resolved': Eticket.objects.filter(status='Solved').count(),  # Resolved tickets
            'unassigned_tickets': Eticket.objects.filter(status='Pending').count(),  # Unassigned (Pending) tickets
            'total_all_pending': Eticket.objects.filter(status='Working').count(),  # Tickets still in progress

            'employees': Employee.objects.all(),
            'accounts': Account.objects.all(),
            'lanrequest': LanRequest.objects.all(),
            'laninstrument': LanInstrument.objects.all(),
            'lantransfer': LanTransfer.objects.all(),
            'laninstrumenttransfer': LanTransferInstrument.objects.all(),
            'file': FileAccess.objects.all(),
            'requisition': Requisition.objects.all(),

            # Total counts
            'employees_total': Employee.objects.count(),
            'accounts_total': Account.objects.count(),
            'lanrequest_total': LanRequest.objects.count(),
            'laninstrument_total': LanInstrument.objects.count(),
            'lantransfer_total': LanTransfer.objects.count(),
            'laninstrumenttransfer_total': LanTransferInstrument.objects.count(),
            'file_total': FileAccess.objects.count(),
            'requisition_total': Requisition.objects.count(),
            
            # Total Approval
            'emp_total': Employee.objects.filter(employee_hr__sign_type='Agreed').count(),
            'account_total': Account.objects.filter(account_hr__sign_type='Agreed').count(),
            'lanrequest_total': LanRequest.objects.filter(lanrequest_sign__sign_type='Agreed').count(),
            'lantransfer_total': LanTransfer.objects.filter(lantransfer_hr__sign_type='Agreed').count(),
            'laninstrument_total': LanInstrument.objects.filter(laninstrument_sign__sign_type='Agreed').count(),
            'laninstrumenttransfer_total': LanTransferInstrument.objects.filter(lantransfer_hr__sign_type='Agreed').count(),
            'file_total': FileAccess.objects.filter(fileaccess_hod__sign_type='Agreed').count(),
            'req_approved': Requisition.objects.filter(requisition_hod_it__sign_type='Agreed',
                requisition_it__admin__first_name__isnull=True
            ).count(),

           # Calculate total form count by adding the counts of each model
            'total_form': (
                Employee.objects.count() +
                Account.objects.count() +
                LanRequest.objects.count() +
                LanInstrument.objects.count() +
                LanTransfer.objects.count() +
                LanTransferInstrument.objects.count() +
                FileAccess.objects.count() +
                Requisition.objects.count()
            ),

            # Calculate total approval by summing the individual totals
            'total_approval': (
                Employee.objects.filter(employee_hr__sign_type='Agreed').count() +
                Account.objects.filter(account_hr__sign_type='Agreed').count() +
                LanRequest.objects.filter(lanrequest_sign__sign_type='Agreed').count() +
                LanTransfer.objects.filter(lantransfer_hr__sign_type='Agreed').count() +
                LanInstrument.objects.filter(laninstrument_sign__sign_type='Agreed').count() +
                LanTransferInstrument.objects.filter(lantransfer_hr__sign_type='Agreed').count() +
                FileAccess.objects.filter(fileaccess_hod__sign_type='Agreed').count() +
                Requisition.objects.filter(
                    requisition_hod_it__sign_type='Agreed',
                    requisition_it__admin__first_name__isnull=True
                ).count()
            ),

            # Calculate total pending as the difference between total forms and total approvals
            'total_pending': (
                (
                    Employee.objects.count() +
                    Account.objects.count() +
                    LanRequest.objects.count() +
                    LanInstrument.objects.count() +
                    LanTransfer.objects.count() +
                    LanTransferInstrument.objects.count() +
                    FileAccess.objects.count() +
                    Requisition.objects.count()
                ) -
                (
                    Employee.objects.filter(employee_hr__sign_type='Agreed').count() +
                    Account.objects.filter(account_hr__sign_type='Agreed').count() +
                    LanRequest.objects.filter(lanrequest_sign__sign_type='Agreed').count() +
                    LanTransfer.objects.filter(lantransfer_hr__sign_type='Agreed').count() +
                    LanInstrument.objects.filter(laninstrument_sign__sign_type='Agreed').count() +
                    LanTransferInstrument.objects.filter(lantransfer_hr__sign_type='Agreed').count() +
                    FileAccess.objects.filter(fileaccess_hod__sign_type='Agreed').count() +
                    Requisition.objects.filter(
                        requisition_hod_it__sign_type='Agreed',
                        requisition_it__admin__first_name__isnull=True
                    ).count()
                )
            )


        })
        return context


   # Custom 403 view function
def custom_403_view(request, exception=None):
    return render(request, 'connectivity/403.html', status=403)
    

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


#--------------------------------------------
# Create your views here.

class ITUserMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class HRUserMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_hr:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class LanListView(ITUserMixin, LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):

        context = {            
            'lans': Lan.objects.all(),
        }
        return render(request, 'blog/lan_home.html', context)


class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'blog/user_it_forms.html'

class AdminHomeView(ITUserMixin, LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):

        context = {            
            'total_users': User.objects.all().count(),
        }
        return render(request, 'blog/admin_home.html', context)

class UserHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/user_home.html'

def test(request):
    return render(request, 'blog/test2.html')

def notifications(request):
    return render(request, 'blog/notification.html')


import io
from PyPDF2 import PdfMerger
from django.http import HttpResponse
from django.test import RequestFactory
from hardware.views import RequisitionPDF
from datetime import datetime

class AdminITFormListView(ITUserMixin, LoginRequiredMixin, ListView):
    model = Requisition
    template_name = 'blog/admin_it_forms.html'
    context_object_name = 'requisition'

    def get_context_data(self, **kwargs):
        # First, get the base context from the superclass
        context = super().get_context_data(**kwargs)

        # Add the custom context variables
        context.update({
            'employees': Employee.objects.all(),
            'emp_total': Employee.objects.filter(employee_hr__sign_type='Agreed').count(),

            'accounts': Account.objects.all(),
            'account_total': Account.objects.filter(account_hr__sign_type='Agreed').count(),

            'requisition': Requisition.objects.all(),
            'req_total': Requisition.objects.all().count(),
            'req_approved': Requisition.objects.filter(
                requisition_hod_it__sign_type='Agreed',
                requisition_it__admin__first_name__isnull=True  # Corrected 'True' spelling
            ).count(),

            'req_chq': Requisition.objects.filter(
                requisition_hod_it__sign_type='Agreed',
                requisition_it__admin__first_name__isnull=False
            ).count(),




            'lanrequest': LanRequest.objects.all(),
            'lanrequest_total': LanRequest.objects.all().filter(lanrequest_sign__sign_type='Agreed').count(),

            'lantransfer': LanTransfer.objects.all(),
            'lantransfer_total': LanTransfer.objects.all().filter(lantransfer_hr__sign_type='Agreed').count(),

            'laninstrument': LanInstrument.objects.all(),
            'laninstrument_total': LanInstrument.objects.all().filter(laninstrument_sign__sign_type='Agreed').count(),

            'laninstrumenttransfer': LanTransferInstrument.objects.all(),
            'laninstrumenttransfer_total': LanTransferInstrument.objects.all().filter(lantransfer_hr__sign_type='Agreed').count(),

            'internet': Internet.objects.all(),
            'internet_total': Internet.objects.all().count(),

            'permission': Permission.objects.all(),
            'permission_total': Permission.objects.all().count(),

            'file': FileAccess.objects.all(),
            'file_total': FileAccess.objects.all().filter(fileaccess_hod__sign_type='Agreed').count(),

            'resignation': Resignation.objects.all(),
            'resignation_total': Resignation.objects.all().count(),
        })

        # Return the updated context
        return context

    from datetime import datetime

    def post(self, request, *args, **kwargs):
        try:
            selected_ids = request.POST.getlist('selected_requisitions')
            form_id = request.POST.get('form_id')

            if selected_ids:
                requisitions = Requisition.objects.filter(pk__in=selected_ids)
                self.send_email_to_chq(requisitions)

                # Number of requisitions processed
                num_requisitions = len(requisitions)

                # Current date and time
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Success message with details
                messages.success(
                    request, 
                    f'Successfully sent an email with {num_requisitions} requisition(s) to CHQ on {current_time}.'
                )
            else:
                messages.error(request, 'No requisitions selected.')

        except Requisition.DoesNotExist:
            messages.error(request, 'One or more selected requisitions do not exist.')

        except Exception as e:
            messages.error(request, f'Error sending email: {str(e)}')

        return redirect('admin-it-forms')


    def send_email_to_chq(self, requisitions):
        try:
            pdf_merger = PdfMerger()

            for requisition in requisitions:
                pdf_content = self.generate_pdf(requisition)
                pdf_merger.append(io.BytesIO(pdf_content))

            merged_pdf = io.BytesIO()
            pdf_merger.write(merged_pdf)
            pdf_merger.close()
            merged_pdf.seek(0)

            profile = Profile.objects.get(user=self.request.user)

            context = {
                'requisitions': requisitions,
                'user': self.request.user,
                'users_profile': profile,
            }

            html_message = render_to_string('blog/e_chq_send.html', context)
            plain_message = strip_tags(html_message)

            current_date = datetime.now().strftime('%Y-%m-%d')

            msg = EmailMultiAlternatives(
                f'Request to Proceed Requisition from SPLU2 on {current_date}',
                plain_message,
                settings.EMAIL_HOST_USER,
                ['fahim.ferdous.335@gmail.com'],
                cc=['fahim.ferdous.335@gmail.com'],
                bcc=['fahim.ferdous.335@gmail.com']
            )
            msg.attach_alternative(html_message, "text/html")
            msg.attach(f'Approved_requisitions_{current_date}.pdf', merged_pdf.read(), 'application/pdf')
            msg.send()

        except Profile.DoesNotExist:
            logger.error("Profile for the current user does not exist.")
            raise Exception("Profile for the current user does not exist.")
        
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            raise e

    def generate_pdf(self, requisition):
        try:
            # Create a mock request using RequestFactory
            request_factory = RequestFactory()
            request = request_factory.get(f'/requisition/{requisition.id}/pdf')

            # Simulate a logged-in user for the mock request
            user = self.request.user  # Assuming this is the user making the request
            request.user = user

            # Instantiate the view that generates the PDF
            requisition_pdf_view = RequisitionPDF.as_view()

            # Simulate the call to the view's `get` method, passing the mock request
            response = requisition_pdf_view(request, pk=requisition.id)

            # Check if the response is successful (status_code == 200)
            if response.status_code != 200:
                raise Exception(f"Failed to generate PDF for Requisition ID {requisition.id}")

            return response.content

        except Exception as e:
            logger.error(f"Error generating PDF for Requisition ID {requisition.id}: {str(e)}")
            raise e



class UserITFormsListView(LoginRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = {
            'employees': Employee.objects.filter(author=user),
            'accounts': Account.objects.filter(author=user),
            'lanrequest': LanRequest.objects.filter(author=user),
            'lantransfer': LanTransfer.objects.filter(author=user),
            'laninstrument': LanInstrument.objects.filter(author=user),
            'laninstrumenttransfer': LanTransferInstrument.objects.filter(author=user),
            'internet': Internet.objects.filter(author=user),
            'permission': Permission.objects.filter(author=user),
            'file': FileAccess.objects.filter(author=user),
            'requisition': Requisition.objects.filter(author=user),
            'resignation': Resignation.objects.filter(author=user),

        }
        return render(request, 'blog/user_it_forms.html', context)

class UserReviewListView(LoginRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        hod_it = User.objects.filter(profile__is_hod_it=True)
        context = {
            'pending': Account.objects.filter(recommended_by=user, account_sign__id__isnull=False),
            'employees': Employee.objects.filter(Q(recommended_by=user) | Q(approved_hod=user) | Q(approved_hr=user)).distinct(),
            'accounts': Account.objects.filter(Q(recommended_by=user) | Q(approved_hod=user) | Q(approved_hr=user)).distinct(),
            'lanrequest': LanRequest.objects.filter(recommended_hod=user),
            'lantransfer': LanTransfer.objects.filter(Q(recommended_hod=user) | Q(recommended_hr=user)).distinct(),
            'laninstrument': LanInstrument.objects.filter(recommended_hod=user),
            'laninstrumenttransfer':  LanTransferInstrument.objects.filter(Q(recommended_hod=user) | Q(recommended_hr=user)).distinct(),
            'internet': Internet.objects.filter(Q(recommended_hod=user) | Q(recommended_hr=user)),
            'permission': Permission.objects.filter(Q(recommended_hod=user) | Q(recommended_hr=user)),
            'file': FileAccess.objects.filter(Q(recommended_by=user) | Q(recommended_hod=user) | Q(other_dept_head=user)),
            'requisition': Requisition.objects.filter(
                Q(recommended_by=user) | Q(recommended_hod=user) | Q(recommended_hr=user) | Q(recommended_hod_it__in=hod_it)
            ).distinct(),
            'resignation': Resignation.objects.filter(
                Q(computer_data_receiver=user) | Q(email_archive_receiver=user) | Q(computer_ip_receiver=user) | 
                Q(ip_phone_receiver=user) | Q(printer_receiever=user) | Q(scanner_receiever=user) |
                Q(recommended_hod=user)),
        }
        return render(request, 'blog/user_review2.html', context)


def display_name(request):

    if request.is_ajax():
        term = request.GET.get('term')
        name_list = User.objects.all().filter(first_name__icontains=term)
        return_recommend = list(name_list.values())
        return JsonResponse(return_recommend, safe=False)

    return HttpResponse('it sends the user first name data')

def display_name_hr(request):

    if request.is_ajax():
        term = request.GET.get('term')        
        name_list = User.objects.all().filter(first_name__icontains=term, profile__is_hr=True)
        return_recommend = list(name_list.values())
        
        return JsonResponse(return_recommend, safe=False)

    return HttpResponse('it sends the HR user first name data')

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


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.object  # Retrieve the current Employee object
        form_id = self.get_object()
        
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        context['author_history'] = User.history.filter(history_date__lte=form_id.date_updated,
                                                        id=form_id.author.id).values().latest()
        context['recommend_history'] = User.history.filter(history_date__lte=form_id.date_updated,
                                                           id=form_id.recommended_by.id).values().latest()
        context['approved_hod_history'] = User.history.filter(history_date__lte=form_id.date_updated,
                                                              id=form_id.approved_hod.id).values().latest()
        
        # Handle approved_hr many-to-many relationship
        context['approved_hr_history'] = [
            User.history.filter(history_date__lte=form_id.date_updated, id=hr_user.id).values().latest()
            for hr_user in form_id.approved_hr.all()
        ]
        
        if hasattr(form_id, 'employee_sign'):                  
            context['signer_history'] = User.history.filter(history_date__lte=form_id.employee_sign.date_updated,
                                                            id=form_id.employee_sign.signer.id).values().latest()
            context['signer_sign'] = 'yes'
        else:
            context['signer_history'] = 'not_signed'

        if hasattr(form_id, 'employee_hod'):                  
            context['hod_history'] = User.history.filter(history_date__lte=form_id.employee_hod.date_updated,
                                                         id=form_id.employee_hod.signer.id).values().latest()
            context['hod_sign'] = 'yes'
        else:
            context['hod_history'] = 'not_signed'

        if hasattr(form_id, 'employee_hr'):                  
            context['hr_history'] = User.history.filter(history_date__lte=form_id.employee_hr.date_updated,
                                                        id=form_id.employee_hr.signer.id).values().latest()
        else:
            context['hr_history'] = 'not_signed'     

        if hasattr(form_id, 'employee_it'):                  
            context['admin_history'] = User.history.filter(history_date__lte=form_id.employee_it.date_updated,
                                                           id=form_id.employee_it.admin.id).values().latest()
        else:
            context['admin_history'] = 'not_signed'        


        context['approved_hr_users'] = employee.approved_hr.all().filter(profile__is_hr=True)


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


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeCreationForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        hr_users = User.objects.filter(profile__is_hr=True)
        form.instance.approved_hr.set(hr_users)
        
        pk = form.instance.pk
        raiser = form.instance.author
        recipient = form.cleaned_data['recommended_by']

        form_id = 'HR-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
        # link = "{settings.WEB_HOST}/employee/" + str(pk) + "/"
        link = f"{settings.WEB_HOST}/employee/{pk}/"


        creation_mail(raiser, pk, [recipient.email], form_id, link)

        return response

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = EmployeeCreationForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        employee = Employee.objects.get(pk=self.kwargs['pk'])
        if request.user != employee.author:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        employee = self.get_object()

        if hasattr(employee, 'employee_it'):
            return HttpResponse('You are not allowed to update as your update time is over.')

        form.instance.author = self.request.user
        response = super().form_valid(form)

        pk = form.instance.pk
        raiser = form.instance.author
        recipient = form.cleaned_data['recommended_by']

        form_id = f'HR-{pk}/{raiser.id}/{raiser.profile.emp_id}'
        link = f"{settings.WEB_HOST}/employee/{pk}/"

        creation_mail(raiser, pk, [recipient.email], form_id, link)
        
        # reviewed_mail(form_id, link, self.request.user)

        hr_users = User.objects.filter(profile__is_hr=True)
        form.instance.approved_hr.set(hr_users)

        return response

    def test_func(self):
        employee = self.get_object()
        return self.request.user == employee.author

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class EmployeeSignCreateView(LoginRequiredMixin, CreateView):
    model = EmployeeSign
    form_class = EmployeeSignForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        employee = Employee.objects.get(pk=self.kwargs['pk'])
        if request.user != employee.recommended_by:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
            form.instance.signer = self.request.user
            form.instance.employee_id = self.kwargs['pk']

            form_id = form.instance.employee
            signer = self.request.user

            # link = "{settings.WEB_HOST}/employee/" + str(form.instance.employee_id) + "/",
            link = f"{settings.WEB_HOST}/employee/{form.instance.employee_id}/"

            if form.instance.sign_type == "Agreed":
                creation_mail(form_id.author, form.instance.employee_id, [form_id.approved_hod.email], form_id, link)
                reviewed_mail(form_id, link, signer)
            if form.instance.sign_type == "Disagreed":
                rejected_mail(form_id, link, signer)

            return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('emp-detail', kwargs={'pk': self.kwargs.get('pk')})

class EmployeeSignUpdateView(LoginRequiredMixin, UpdateView):
    model = EmployeeSign
    form_class = EmployeeSignForm

    # Ensure the dispatch method is working by checking user permissions
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        employee_sign = self.get_object()  # Get the EmployeeSign object
        employee = employee_sign.employee  # Get the associated Employee object
        
        # Check if the user is allowed to update (e.g., if they recommended the employee)
        if request.user != employee.recommended_by:
            return custom_403_view(request)
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        employee_sign = self.get_object()
            
        if hasattr(employee_sign.employee, 'employee_hod'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
            
        form_id = form.instance.employee
        signer = self.request.user

        # link = "{settings.WEB_HOST}/employee/" + str(form.instance.employee_id) + "/",
        link = f"{settings.WEB_HOST}/employee/{form.instance.employee_id}/"

        if form.instance.sign_type == "Agreed":
            creation_mail(form_id.author, form.instance.employee_id, [form_id.approved_hod.email], form_id, link)
            reviewed_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)

        return super().form_valid(form)

    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('emp-detail', kwargs={'pk': form_id.employee.id })




#--------------------------------Account HOD View--------------------------------------------
class EmployeeHODCreateView(LoginRequiredMixin, CreateView):
    model = EmployeeHOD
    form_class = EmployeeHODForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        employee = Employee.objects.get(pk=self.kwargs['pk'])
        if request.user != employee.approved_hod:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.employee_id = self.kwargs['pk']

        form_id = form.instance.employee
        signer = self.request.user

        link = f"{settings.WEB_HOST}/employee/{form.instance.employee_id}/"

        if form.instance.sign_type == "Agreed":
            recipient_emails = [user.email for user in form_id.approved_hr.all()]
            creation_mail(form_id.author, form.instance.employee_id, recipient_emails, form_id, link)
            reviewed_mail(form_id, link, signer)
            
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
        
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('emp-detail', kwargs={'pk': self.kwargs.get('pk')})

class EmployeeHODUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EmployeeHOD
    form_class = EmployeeHODForm


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        employee_hod = self.get_object()  # Get the EmployeeSign object
        employee = employee_hod.employee  # Get the associated Employee object
        
        # Check if the user is allowed to update (e.g., if they recommended the employee)
        if request.user != employee.approved_hod:
            return custom_403_view(request)
        
        return super().dispatch(request, *args, **kwargs)
        

    def form_valid(self, form):
        employee_hod = self.get_object()
            
        if hasattr(employee_hod.employee, 'employee_hr'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
            
        form_id = form.instance.employee
        signer = self.request.user

        link = f"{settings.WEB_HOST}/employee/{form.instance.employee_id}/"

        if form.instance.sign_type == "Agreed":
            recipient_emails = [user.email for user in form_id.approved_hr.all()]
            creation_mail(form_id.author, form.instance.employee_id, recipient_emails, form_id, link)
            reviewed_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
        
        return super().form_valid(form)

    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('emp-detail', kwargs={'pk': form_id.employee.id })

#--------------------------------Account HR View--------------------------------------------
class EmployeeHRCreateView(LoginRequiredMixin, CreateView):
    model = EmployeeHR
    form_class = EmployeeHRForm


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        employee = Employee.objects.get(pk=self.kwargs['pk'])
        if request.user not in employee.approved_hr.all():
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.employee_id = self.kwargs['pk']

        form_id = form.instance.employee
        signer = self.request.user

        link = f"{settings.WEB_HOST}/employee/{form.instance.employee_id}/"

        if form.instance.sign_type == "Agreed":
            # reviewed_mail(form_id, link, signer)
            approved_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
            
        #=========================Create TIcket========================================
        if form.instance.sign_type == "Agreed":
            category = ProblemCategory.objects.get(id='5')
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
        return reverse('emp-detail', kwargs={'pk': self.kwargs.get('pk')})

class EmployeeHRUpdateView(LoginRequiredMixin,  HRUserMixin , UpdateView):
    model = EmployeeHR
    form_class = EmployeeHRForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        employee_hr = self.get_object()  # Get the EmployeeSign object
        employee = employee_hr.employee  # Get the associated Employee object
        
        # Check if the user is allowed to update (e.g., if they recommended the employee)
        if request.user not in employee.approved_hr.all():
            return custom_403_view(request)
        
        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        employee_hr = self.get_object()
            
        if hasattr(employee_hr.employee, 'employee_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
            
        form_id = form.instance.employee
        signer = self.request.user

        link = f"{settings.WEB_HOST}/employee/{form.instance.employee_id}/"

        if form.instance.sign_type == "Agreed":
            # reviewed_mail(form_id, link, signer)
            approved_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
            
        #=========================Create TIcket========================================
        if form.instance.sign_type == "Agreed":
            category = ProblemCategory.objects.get(id='5')
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
        employee = self.get_object()
        if self.request.user == employee.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('emp-detail', kwargs={'pk': form_id.employee.id })


class EmployeeITCreateView(LoginRequiredMixin, ITUserMixin ,CreateView):
    model = EmployeeIT
    form_class = EmployeeITForm

    def form_valid(self, form):
        form.instance.admin = self.request.user
        form.instance.employee_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('emp-detail', kwargs={'pk': self.kwargs.get('pk')})

class EmployeeITUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = EmployeeIT
    form_class = EmployeeITForm

    def form_valid(self, form):
        form_id = self.get_object()       
        form.instance.admin = self.request.user
        form.instance.employee_id = form_id.employee.id
        response = super().form_valid(form)
        return response
            
    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.admin:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('emp-detail', kwargs={'pk': form_id.employee.id })


class EmployeePDF(LoginRequiredMixin, View):
    model = Employee
    
    def get(self, request, pk, *args, **kwargs):
        aa = self.kwargs.get('pk')
        form_id = Employee.objects.get(pk=aa)


        if hasattr(form_id, 'employee_sign'):                  
            signer_history = User.history.filter(history_date__lte = form_id.employee_sign.date_signed,
                                                            id = form_id.employee_sign.signer.id).values().latest()
        else:
            signer_history = 'not_signed'

        if hasattr(form_id, 'employee_hod'):                  
            hod_history = User.history.filter(history_date__lte = form_id.employee_hod.date_signed,
                                                            id = form_id.employee_hod.signer.id).values().latest()
        else:
            hod_history = 'not_signed'
        
        if hasattr(form_id, 'employee_hr'):                  
            hr_history = User.history.filter(history_date__lte = form_id.employee_hr.date_signed,
                                                            id = form_id.employee_hr.signer.id).values().latest()
        else:
            hr_history = 'not_signed'

        if hasattr(form_id, 'employee_it'):                  
            admin_history = User.history.filter(history_date__lte = form_id.employee_it.date_signed,
                                                            id = form_id.employee_it.admin.id).values().latest()
        else:
            admin_history = 'not_signed'

        data = {
            'runset': form_id,
            'author_history': User.history.filter(history_date__lte = form_id.date_posted,
                                                id = form_id.author.id).values().latest(),

            'signer_history' : signer_history,
            'hod_history': hod_history,
            'hr_history': hr_history,
            'admin_history' : admin_history,  
            'user_activation_choices': dict(form_id._meta.get_field('user_activation').choices),
            'mail_activation_choices': dict(form_id._meta.get_field('mail_activation').choices),
            'group_access_choices': dict(form_id._meta.get_field('group_access').choices),


        }
        pdf = render_to_pdf('blog/employee_pdf.html', data)
        # print(signer_history) 
        return HttpResponse(pdf, content_type='application/pdf')


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        account = self.object  # Retrieve the current Employee object
        form_id = self.get_object()
        
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        context['user_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.author.id).values().latest()
        context['profile_history'] = Profile.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.author.profile.id)
        context['recommend_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.recommended_by.id).values().latest()
        context['approved_hod_history'] = User.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.approved_hod.id).values().latest()

        # context['approved_hr_history'] = User.history.filter(history_date__lte = form_id.date_updated,
        #                                                     id = form_id.approved_hr.id).values().latest()

        context['approved_hr_history'] = [
            User.history.filter(history_date__lte=form_id.date_updated, id=hr_user.id).values().latest()
            for hr_user in form_id.approved_hr.all()
        ]


        if hasattr(form_id, 'account_sign'):                  
            context['signer_history'] = User.history.filter(history_date__lte = form_id.account_sign.date_updated,
                                                            id = form_id.account_sign.signer.id).values().latest()
            context['signer_sign'] = 'yes'
        else:
            context['signer_history'] = 'not_signed'

        if hasattr(form_id, 'account_hod'):                  
            context['hod_history'] = User.history.filter(history_date__lte = form_id.account_hod.date_updated,
                                                            id = form_id.account_hod.signer.id).values().latest()
            context['hod_sign'] = 'yes'
        else:
            context['hod_history'] = 'not_signed'

        if hasattr(form_id, 'account_hr'):                  
            context['hr_history'] = User.history.filter(history_date__lte = form_id.account_hr.date_updated,
                                                            id = form_id.account_hr.signer.id).values().latest()
        else:
            context['hr_history'] = 'not_signed' 

        if hasattr(form_id, 'account_it'):                  
            context['admin_history'] = User.history.filter(history_date__lte = form_id.account_it.date_updated,
                                                            id = form_id.account_it.admin.id).values().latest()
        else:
            context['admin_history'] = 'not_signed' 

        context['approved_hr_users'] = account.approved_hr.all().filter(profile__is_hr=True)



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


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountCreationForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        hr_users = User.objects.filter(profile__is_hr=True)
        form.instance.approved_hr.set(hr_users)
        
        pk = form.instance.pk
        raiser = form.instance.author
        recipient = form.cleaned_data['recommended_by']

        form_id = 'MUAC-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
        # link = "{settings.WEB_HOST}/account/" + str(pk) + "/"
        link = f"{settings.WEB_HOST}/account/{pk}/"


        creation_mail(raiser, pk, [recipient.email], form_id, link)

        return response

class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Account
    form_class = AccountCreationForm


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        account = Account.objects.get(pk=self.kwargs['pk'])
        if request.user != account.author:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        Account = self.get_object()


        if hasattr(Account, 'Account_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.author = self.request.user
            response = super().form_valid(form)

            pk = form.instance.pk
            raiser = form.instance.author
            recipient_by = form.cleaned_data['recommended_by']
            recipient_hod = form.cleaned_data['approved_hod']
            recipient_hr = form.cleaned_data['approved_hr']

            form_id = 'MUAC-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
            # link = "{settings.WEB_HOST}/account/" + str(pk) + "/"
            link = f"{settings.WEB_HOST}/account/{pk}/"

            if not hasattr(Account, 'Account_sign'):         
                if Account.recommended_by != recipient_by:
                    creation_mail(raiser, pk, [recipient_by.email], form_id, link)

            if hasattr(Account, 'Account_sign') and (not hasattr(Account, 'Account_hod')):  
                if Account.approved_hod != recipient_hod:
                    creation_mail(raiser, pk, [recipient_hod.email], form_id, link)
                
            if hasattr(Account, 'Account_hod') and (not hasattr(Account, 'Account_hr')): 
                if Account.approved_hr != recipient_hr:
                    creation_mail(raiser, pk, [recipient_hr.email], form_id, link)

            
            hr_users = User.objects.filter(profile__is_hr=True)
            form.instance.approved_hr.set(hr_users)

            return response

    def test_func(self):
        Account = self.get_object()
        if self.request.user == Account.author:
            return True
        return False


#--------------------------------Account Sign View-----------------------------------------
class AccountSignCreateView(LoginRequiredMixin, CreateView):
    model = AccountSign
    form_class = AccountSignForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        account = Account.objects.get(pk=self.kwargs['pk'])
        if request.user != account.recommended_by:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.account_id = self.kwargs['pk']

        form_id = form.instance.account
        signer = self.request.user

        # link = "{settings.WEB_HOST}/account/" + str(form.instance.account_id) + "/"
        link = f"{settings.WEB_HOST}/account/{form.instance.account_id}/"

        if form.instance.sign_type == "Agreed":
            creation_mail(form_id.author, form.instance.account_id, [form_id.approved_hod.email], form_id, link)
            reviewed_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('mail-detail', kwargs={'pk': self.kwargs.get('pk')})


class AccountSignUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AccountSign
    form_class = AccountSignForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        account_sign = self.get_object()
        account = account_sign.account
        if request.user != account.recommended_by:
            return custom_403_view(request)  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        account_sign = self.get_object()
            
        if hasattr(account_sign.account, 'account_hod'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
            
        form_id = form.instance.account
        signer = self.request.user

        link = f"{settings.WEB_HOST}/account/{form.instance.account_id}/"

        if form.instance.sign_type == "Agreed":
            creation_mail(form_id.author, form.instance.account_id, [form_id.approved_hod.email], form_id, link)
            reviewed_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)

        return super().form_valid(form)

    def test_func(self):
        account = self.get_object()
        if self.request.user == account.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('mail-detail', kwargs={'pk': form_id.account.id })

#--------------------------------Account HOD View--------------------------------------------
class AccountHODCreateView(LoginRequiredMixin, CreateView):
    model = AccountHOD
    form_class = AccountHODForm


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        account = Account.objects.get(pk=self.kwargs['pk'])
        if request.user != account.approved_hod:
            return custom_403_view(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.account_id = self.kwargs['pk']

        form_id = form.instance.account
        signer = self.request.user

        link = f"{settings.WEB_HOST}/employee/{form.instance.account_id}/"

        if form.instance.sign_type == "Agreed":
            recipient_emails = [user.email for user in form_id.approved_hr.all()]
            creation_mail(form_id.author, form.instance.account_id, recipient_emails, form_id, link)
            reviewed_mail(form_id, link, signer)
            
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
        
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('mail-detail', kwargs={'pk': self.kwargs.get('pk')})

class AccountHODUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AccountHOD
    form_class = AccountHODForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        account_hod = self.get_object()
        account = account_hod.account
        if request.user != account.approved_hod:
            return custom_403_view(request)  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        account_hod = self.get_object()
            
        if hasattr(account_hod.account, 'account_hr'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
            
        form_id = form.instance.account
        signer = self.request.user

        link = f"{settings.WEB_HOST}/employee/{form.instance.account_id}/"

        if form.instance.sign_type == "Agreed":
            recipient_emails = [user.email for user in form_id.approved_hr.all()]
            creation_mail(form_id.author, form.instance.account_id, recipient_emails, form_id, link)
            reviewed_mail(form_id, link, signer)
            
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
        
        return super().form_valid(form)

    def test_func(self):
        account = self.get_object()
        if self.request.user == account.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('mail-detail', kwargs={'pk': form_id.account.id })

#--------------------------------Account HR View--------------------------------------------
class AccountHRCreateView(LoginRequiredMixin, HRUserMixin, CreateView):
    model = AccountHR
    form_class = AccountHRForm

    @method_decorator(login_required, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        account = Account.objects.get(pk=self.kwargs['pk'])
        if request.user not in account.approved_hr.all():
            return custom_403_view(request)  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.account_id = self.kwargs['pk']

        form_id = form.instance.account
        signer = self.request.user

        link = f"{settings.WEB_HOST}/account/{form.instance.account_id}/"
        
        if form.instance.sign_type == "Agreed":
            approved_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
            
        #=========================Create TIcket========================================
        if form.instance.sign_type == "Agreed":
            category = ProblemCategory.objects.get(id='5')
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
        return reverse('mail-detail', kwargs={'pk': self.kwargs.get('pk')})

class AccountHRUpdateView(LoginRequiredMixin,  HRUserMixin, UpdateView):
    model = AccountHR
    form_class = AccountHRForm


    @method_decorator(login_required, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        account_hr = self.get_object()
        account = account_hr.account
        if request.user not in account.approved_hr.all():
            return custom_403_view(request) 
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        account_hr = self.get_object()
            
        if hasattr(account_hr.account, 'account_it'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
            
        form_id = form.instance.account
        signer = self.request.user

        link = f"{settings.WEB_HOST}/account/{form.instance.account_id}/"
        
        if form.instance.sign_type == "Agreed":
            approved_mail(form_id, link, signer)
        if form.instance.sign_type == "Disagreed":
            rejected_mail(form_id, link, signer)
            
        #=========================Create TIcket========================================
        if form.instance.sign_type == "Agreed":
            category = ProblemCategory.objects.get(id='5')
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
        account = self.get_object()
        if self.request.user == account.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('mail-detail', kwargs={'pk': form_id.account.id })

#--------------------------------Account IT View--------------------------------------------
class AccountITCreateView(LoginRequiredMixin, CreateView):
    model = AccountIT
    form_class = AccountITForm

    def form_valid(self, form):
        form.instance.admin = self.request.user
        form.instance.account_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('mail-detail', kwargs={'pk': self.kwargs.get('pk')})

class AccountITUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = AccountIT
    form_class = AccountITForm
    
    def form_valid(self, form):
        form_id = self.get_object()       
        form.instance.signer = self.request.user
        form.instance.account_id = form_id.account.id
        response = super().form_valid(form)
        return response

    def test_func(self):
        account = self.get_object()
        if self.request.user == account.admin:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('mail-detail', kwargs={'pk': form_id.account.id })


class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Account
    success_url = '/'

    def test_func(self):
        account = self.get_object()
        if self.request.user == account.author:
            return True
        return False


# Opens up page as PDF
#---------------------------------------Account PDF------------------------------------
class AccountPDF(View):
    model = Account
    
    def get(self, request, pk, *args, **kwargs):
        
        aa = self.kwargs.get('pk')
        form_id = Account.objects.get(pk=aa)
 
        if hasattr(form_id, 'account_sign'):                  
            signer_history = User.history.filter(history_date__lte = form_id.account_sign.date_updated,
                                                            id = form_id.account_sign.signer.id).values().latest()
        else:
            signer_history = 'not_signed'

        if hasattr(form_id, 'account_hod'):                  
            hod_history = User.history.filter(history_date__lte = form_id.account_hod.date_updated,
                                                            id = form_id.account_hod.signer.id).values().latest()
        else:
            hod_history = 'not_signed'

        if hasattr(form_id, 'account_hr'):                  
            hr_history = User.history.filter(history_date__lte = form_id.account_hr.date_updated,
                                                            id = form_id.account_hr.signer.id).values().latest()
        else:
            hr_history = 'not_signed'


        if hasattr(form_id, 'account_it'):                  
            admin_history = User.history.filter(history_date__lte = form_id.account_it.date_updated,
                                                            id = form_id.account_it.admin.id).values().latest()
        else:
            admin_history = 'not_signed'

        data = {
            'runset': form_id,
            'user_history': User.history.filter(history_date__lte = form_id.date_updated,
                                                id = form_id.author.id).values().latest(),

            'profile_history': Profile.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.author.profile.id),

            'signer_history' : signer_history,
            'hod_history': hod_history,
            'hr_history': hr_history,
            'admin_history' : admin_history,  
            'user_activation_choices': dict(form_id._meta.get_field('user_activation').choices),
            'mail_activation_choices': dict(form_id._meta.get_field('mail_activation').choices),
            'group_access_choices': dict(form_id._meta.get_field('group_access').choices),

        }
        pdf = render_to_pdf('blog/account_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class AccountDownloadPDF(LoginRequiredMixin, View):
    model = Account
    def get(self, request, *args, **kwargs):
        data = {
            'runset': Account.objects.get(pk=self.kwargs.get('pk')),
        }

        pdf = render_to_pdf('blog/account_pdf.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response

class ResignationDetailView(LoginRequiredMixin, DetailView):
    model = Resignation

    def get_context_data(self, **kwargs):

        context = super(ResignationDetailView, self).get_context_data(**kwargs)
        form_id = self.get_object()                
        
        context['user_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.author.id).values().latest()
        context['profile_history'] = Profile.history.filter(history_date__lte = form_id.date_updated, 
                                                            id = form_id.author.profile.id)
        
        context['data_receiver_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.computer_data_receiver.id).values().latest()
        context['email_archiver_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.email_archive_receiver.id).values().latest()
        context['ip_receiver_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.computer_ip_receiver.id).values().latest()

        
        if form_id.ip_phone_receiver is not None:        
            context['phone_receiver_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.ip_phone_receiver.id).values().latest()      
        
        if form_id.printer_receiever is not None:
            context['printer_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.printer_receiever.id).values().latest()
        if form_id.scanner_receiever is not None:
            context['scanner_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.scanner_receiever.id).values().latest()                                                    

        context['recommend_hod_history'] = User.history.filter(history_date__lte = form_id.date_updated,
                                                            id = form_id.recommended_hod.id).values().latest()

        #------------------------------------Signer History-----------------------------------
        if hasattr(form_id, 'resignation_data'):                  
            context['data_signer'] = User.history.filter(history_date__lte = form_id.resignation_data.date_updated,
                                                            id = form_id.resignation_data.signer.id).values().latest()
        else:
            context['data_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_archive'):                  
            context['archive_signer'] = User.history.filter(history_date__lte = form_id.resignation_archive.date_updated,
                                                            id = form_id.resignation_archive.signer.id).values().latest()
        else:
            context['archive_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_ip'):                  
            context['ip_signer'] = User.history.filter(history_date__lte = form_id.resignation_ip.date_updated,
                                                            id = form_id.resignation_ip.signer.id).values().latest()
        else:
            context['ip_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_phone'):                  
            context['phone_signer'] = User.history.filter(history_date__lte = form_id.resignation_phone.date_updated,
                                                            id = form_id.resignation_phone.signer.id).values().latest()
        else:
            context['phone_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_printer'):                  
            context['printer_signer'] = User.history.filter(history_date__lte = form_id.resignation_printer.date_updated,
                                                            id = form_id.resignation_printer.signer.id).values().latest()
        else:
            context['printer_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_scanner'):                  
            context['scanner_signer'] = User.history.filter(history_date__lte = form_id.resignation_scanner.date_updated,
                                                            id = form_id.resignation_scanner.signer.id).values().latest()
        else:
            context['scanner_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_hod'):                  
            context['hod_signer'] = User.history.filter(history_date__lte = form_id.resignation_hod.date_updated,
                                                            id = form_id.resignation_hod.signer.id).values().latest()
        else:
            context['hod_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_internet'):                  
            context['internet_signer'] = User.history.filter(history_date__lte = form_id.resignation_internet.date_updated,
                                                            id = form_id.resignation_internet.signer.id).values().latest()
        else:
            context['internet_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_empower'):                  
            context['empower_signer'] = User.history.filter(history_date__lte = form_id.resignation_empower.date_updated,
                                                            id = form_id.resignation_empower.signer.id).values().latest()
        else:
            context['empower_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_chromeleon'):                  
            context['chromeleon_signer'] = User.history.filter(history_date__lte = form_id.resignation_chromeleon.date_updated,
                                                            id = form_id.resignation_chromeleon.signer.id).values().latest()
        else:
            context['chromeleon_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_eqms'):                  
            context['eqms_signer'] = User.history.filter(history_date__lte = form_id.resignation_eqms.date_updated,
                                                            id = form_id.resignation_eqms.signer.id).values().latest()
        else:
            context['eqms_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_standalone'):                  
            context['standalone_signer'] = User.history.filter(history_date__lte = form_id.resignation_standalone.date_updated,
                                                            id = form_id.resignation_standalone.signer.id).values().latest()
        else:
            context['standalone_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_disable'):                  
            context['disable_signer'] = User.history.filter(history_date__lte = form_id.resignation_disable.date_updated,
                                                            id = form_id.resignation_disable.signer.id).values().latest()
        else:
            context['disable_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_primary'):                  
            context['primary_signer'] = User.history.filter(history_date__lte = form_id.resignation_primary.date_updated,
                                                            id = form_id.resignation_primary.signer.id).values().latest()
        else:
            context['primary_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_deletion'):                  
            context['deletion_signer'] = User.history.filter(history_date__lte = form_id.resignation_deletion.date_updated,
                                                            id = form_id.resignation_deletion.signer.id).values().latest()
        else:
            context['deletion_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_final'):                  
            context['final_signer'] = User.history.filter(history_date__lte = form_id.resignation_final.date_updated,
                                                            id = form_id.resignation_final.signer.id).values().latest()
        else:
            context['final_signer'] = 'not_signed'

                                            
        return context


class ResignationCreateView(LoginRequiredMixin, CreateView):
    model = Resignation
    form_class = ResignationCreationForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        pk = form.instance.pk
        raiser = form.instance.author
                
        datar = form.cleaned_data['computer_data_receiver']
        archiver = form.cleaned_data['email_archive_receiver']
        ipr = form.cleaned_data['computer_ip_receiver']        
        ip_phoner = form.cleaned_data['ip_phone_receiver']
        printerr = form.cleaned_data['printer_receiever']
        scannerr = form.cleaned_data['scanner_receiever']
        hod = form.cleaned_data['recommended_hod']

        recipient = {datar.email, archiver.email, ipr.email, hod.email}

        if printerr is not None:
            recipient.add(printerr.email) 
        if scannerr is not None:
            recipient.add(scannerr.email)
        if ip_phoner is not None:
            recipient.add(ip_phoner.email)

        form_id = 'RESG-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
        link = "{settings.WEB_HOST}/resignation/" + str(pk) + "/"

        creation_mail(raiser, pk, list(recipient), form_id, link)

        return response

class ResignationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resignation
    form_class = ResignationCreationForm
    # fields = ResignationCreationForm

    def form_valid(self, form):        
        resignation = self.get_object()

        if hasattr(resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.author = self.request.user
            response = super().form_valid(form)

            pk = form.instance.pk
            raiser = form.instance.author

            datar = form.cleaned_data['computer_data_receiver']
            archiver = form.cleaned_data['email_archive_receiver']
            ipr = form.cleaned_data['computer_ip_receiver']        
            ip_phoner = form.cleaned_data['ip_phone_receiver']
            printerr = form.cleaned_data['printer_receiever']
            scannerr = form.cleaned_data['scanner_receiever']
            hod = form.cleaned_data['recommended_hod']

            form_id = 'RESG-' + str(pk) + '/' + str(raiser.id) + '/' + str(raiser.profile.emp_id)
            link = "{settings.WEB_HOST}/resignation/" + str(pk) + "/"


            # if printerr is None or scannerr is None:
            #     recipient = list({datar.email, archiver.email, ipr.email,
            #                 ip_phoner.email, hod.email})
                        
            # else:
            #     recipient = list({datar.email, archiver.email, ipr.email,ip_phoner.email,
            #             printerr.email, scannerr.email, hod.email})

            # creation_mail(raiser, pk, recipient, form_id, link)

            return response

    def test_func(self):
        account = self.get_object()
        if self.request.user == account.author:
            return True
        return False

#--------------------------------------Resignation Computer Data--------------------------------------------

class ResignationDataCreateView(LoginRequiredMixin, CreateView):
    model = ResignationData
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']
        form_id = form.instance.resignation
        signer = self.request.user

        link = "{settings.WEB_HOST}/resignation/" + str(form.instance.resignation_id) + "/"
        reviewed_mail(form_id, link, signer)

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationDataUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ResignationData
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()
        if hasattr(form_id.resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })


#--------------------------------------Resignation Email Archive--------------------------------------------

class ResignationArchiveCreateView(LoginRequiredMixin, CreateView):
    model = ResignationArchive
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']

        form_id = form.instance.resignation
        signer = self.request.user
        link = "{settings.WEB_HOST}/resignation/" + str(form.instance.resignation_id) + "/"

        reviewed_mail(form_id, link, signer)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationArchiveUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ResignationArchive
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })

#--------------------------------------Resignation Computer IP--------------------------------------------

class ResignationIPCreateView(LoginRequiredMixin, CreateView):
    model = ResignationIP
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']

        form_id = form.instance.resignation
        signer = self.request.user
        link = "{settings.WEB_HOST}/resignation/" + str(form.instance.resignation_id) + "/"

        reviewed_mail(form_id, link, signer)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationIPUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ResignationIP
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })


#--------------------------------------Resignation Computer IP--------------------------------------------

class ResignationPhoneCreateView(LoginRequiredMixin, CreateView):
    model = ResignationPhone
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']

        form_id = form.instance.resignation
        signer = self.request.user
        link = "{settings.WEB_HOST}/resignation/" + str(form.instance.resignation_id) + "/"

        reviewed_mail(form_id, link, signer)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationPhoneUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ResignationPhone
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })


#--------------------------------------Resignation Computer IP--------------------------------------------

class ResignationPrinterCreateView(LoginRequiredMixin, CreateView):
    model = ResignationPrinter
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']

        form_id = form.instance.resignation
        signer = self.request.user
        link = "{settings.WEB_HOST}/resignation/" + str(form.instance.resignation_id) + "/"

        reviewed_mail(form_id, link, signer)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationPrinterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ResignationPrinter
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })

#--------------------------------------Resignation Computer IP--------------------------------------------

class ResignationScannerCreateView(LoginRequiredMixin, CreateView):
    model = ResignationScanner
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']

        form_id = form.instance.resignation
        signer = self.request.user
        link = "{settings.WEB_HOST}/resignation/" + str(form.instance.resignation_id) + "/"

        reviewed_mail(form_id, link, signer)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationScannerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ResignationScanner
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })


#--------------------------------------Resignation Computer IP--------------------------------------------

class ResignationHODCreateView(LoginRequiredMixin, CreateView):
    model = ResignationHOD
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']

        form_id = form.instance.resignation
        signer = self.request.user
        link = "{settings.WEB_HOST}/resignation/" + str(form.instance.resignation_id) + "/"

        reviewed_mail(form_id, link, signer)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationHODUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ResignationHOD
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })


#--------------------------------------Resignation Internet--------------------------------------------

class ResignationInternetCreateView(LoginRequiredMixin, CreateView):
    model = ResignationInternet
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']

        form_id = form.instance.resignation
        signer = self.request.user
        link = "{settings.WEB_HOST}/resignation/" + str(form.instance.resignation_id) + "/"

        reviewed_mail(form_id, link, signer)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationInternetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ResignationInternet
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })

#--------------------------------------Resignation Empower--------------------------------------------

class ResignationEmpowerCreateView(LoginRequiredMixin, ITUserMixin, CreateView):
    model = ResignationEmpower
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']

        form_id = form.instance.resignation
        signer = self.request.user
        link = "{settings.WEB_HOST}/resignation/" + str(form.instance.resignation_id) + "/"

        reviewed_mail(form_id, link, signer)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationEmpowerUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = ResignationEmpower
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })

#--------------------------------------Resignation Chromeleon--------------------------------------------

class ResignationChromeleonCreateView(LoginRequiredMixin, ITUserMixin, CreateView):
    model = ResignationChromeleon
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']

        form_id = form.instance.resignation
        signer = self.request.user
        link = "{settings.WEB_HOST}/resignation/" + str(form.instance.resignation_id) + "/"

        reviewed_mail(form_id, link, signer)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationChromeleonUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = ResignationChromeleon
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })

#--------------------------------------Resignation EMQS--------------------------------------------

class ResignationEqmsCreateView(LoginRequiredMixin, ITUserMixin, CreateView):
    model = ResignationEqms
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']

        form_id = form.instance.resignation
        signer = self.request.user
        link = "{settings.WEB_HOST}/resignation/" + str(form.instance.resignation_id) + "/"

        reviewed_mail(form_id, link, signer)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationEqmsUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = ResignationEqms
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })


#--------------------------------------Resignation Standalone--------------------------------------------

class ResignationStandaloneCreateView(LoginRequiredMixin, ITUserMixin, CreateView):
    model = ResignationStandalone
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']

        form_id = form.instance.resignation
        signer = self.request.user
        link = "{settings.WEB_HOST}/resignation/" + str(form.instance.resignation_id) + "/"

        reviewed_mail(form_id, link, signer)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationStandaloneUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = ResignationStandalone
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_disable'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })

#--------------------------------------Resignation Mail Disable--------------------------------------------

class ResignationDisableCreateView(LoginRequiredMixin, ITUserMixin, CreateView):
    model = ResignationDisable
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationDisableUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = ResignationDisable
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_primary'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })

#--------------------------------------Resignation Primary Sign--------------------------------------------

class ResignationPrimaryCreateView(LoginRequiredMixin, ITUserMixin, CreateView):
    model = ResignationPrimary
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationPrimaryUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = ResignationPrimary
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_deletion'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })

#--------------------------------------Resignation Deletion--------------------------------------------

class ResignationDeletionCreateView(LoginRequiredMixin, ITUserMixin, CreateView):
    model = ResignationDeletion
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationDeletionUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = ResignationDeletion
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        if hasattr(form_id.resignation, 'resignation_final'):
            return HttpResponse('You are not allowed to update as your update time is over.!!!')
        else:
            form.instance.signer = self.request.user
            form.instance.resignation_id = form_id.resignation.id
            return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })


#--------------------------------------Resignation FInal and Closed--------------------------------------------

class ResignationFinalCreateView(LoginRequiredMixin, ITUserMixin, CreateView):
    model = ResignationFinal
    fields = ['sign_type', 'comment']

    def form_valid(self, form):
        form.instance.signer = self.request.user
        form.instance.resignation_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('resignation-detail', kwargs={'pk': self.kwargs.get('pk')})

class ResignationFinalUpdateView(LoginRequiredMixin, UserPassesTestMixin, ITUserMixin, UpdateView):
    model = ResignationFinal
    fields = ['sign_type', 'comment']

    def form_valid(self, form):        
        form_id = self.get_object()       
        form.instance.signer = self.request.user
        form.instance.resignation_id = form_id.resignation.id
        return super().form_valid(form)
            
    def test_func(self):
        resignation = self.get_object()
        if self.request.user == resignation.signer:
            return True
        return False

    def get_success_url(self, **kwargs):
        form_id = self.get_object()
        return reverse('resignation-detail', kwargs={'pk': form_id.resignation.id })
#--------------------------------------Resignation PDF--------------------------------------------
class ResignationPDF(LoginRequiredMixin, View):
    model = Resignation
    
    def get(self, request, pk, *args, **kwargs):
        
        aa = self.kwargs.get('pk')
        form_id = Resignation.objects.get(pk=aa)

        context = {
            'runset': form_id,
        }

        context['user_history'] = User.history.filter(history_date__lte = form_id.date_posted,
                                                            id = form_id.author.id).values().latest()
        context['profile_history'] = Profile.history.filter(history_date__lte = form_id.date_posted, 
                                                            id = form_id.author.profile.id)
        
         #------------------------------------Signer History-----------------------------------
        if hasattr(form_id, 'resignation_data'):                  
            context['data_signer'] = User.history.filter(history_date__lte = form_id.resignation_data.date_updated,
                                                            id = form_id.resignation_data.signer.id).values().latest()
        else:
            context['data_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_archive'):                  
            context['archive_signer'] = User.history.filter(history_date__lte = form_id.resignation_archive.date_updated,
                                                            id = form_id.resignation_archive.signer.id).values().latest()
        else:
            context['archive_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_ip'):                  
            context['ip_signer'] = User.history.filter(history_date__lte = form_id.resignation_ip.date_updated,
                                                            id = form_id.resignation_ip.signer.id).values().latest()
        else:
            context['ip_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_phone'):                  
            context['phone_signer'] = User.history.filter(history_date__lte = form_id.resignation_phone.date_updated,
                                                            id = form_id.resignation_phone.signer.id).values().latest()
        else:
            context['phone_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_printer'):                  
            context['printer_signer'] = User.history.filter(history_date__lte = form_id.resignation_printer.date_updated,
                                                            id = form_id.resignation_printer.signer.id).values().latest()
        else:
            context['printer_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_scanner'):                  
            context['scanner_signer'] = User.history.filter(history_date__lte = form_id.resignation_scanner.date_updated,
                                                            id = form_id.resignation_scanner.signer.id).values().latest()
        else:
            context['scanner_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_hod'):                  
            context['hod_signer'] = User.history.filter(history_date__lte = form_id.resignation_hod.date_updated,
                                                            id = form_id.resignation_hod.signer.id).values().latest()
        else:
            context['hod_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_internet'):                  
            context['internet_signer'] = User.history.filter(history_date__lte = form_id.resignation_internet.date_updated,
                                                            id = form_id.resignation_internet.signer.id).values().latest()
        else:
            context['internet_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_empower'):                  
            context['empower_signer'] = User.history.filter(history_date__lte = form_id.resignation_empower.date_updated,
                                                            id = form_id.resignation_empower.signer.id).values().latest()
        else:
            context['empower_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_chromeleon'):                  
            context['chromeleon_signer'] = User.history.filter(history_date__lte = form_id.resignation_chromeleon.date_updated,
                                                            id = form_id.resignation_chromeleon.signer.id).values().latest()
        else:
            context['chromeleon_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_eqms'):                  
            context['eqms_signer'] = User.history.filter(history_date__lte = form_id.resignation_eqms.date_updated,
                                                            id = form_id.resignation_eqms.signer.id).values().latest()
        else:
            context['eqms_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_standalone'):                  
            context['standalone_signer'] = User.history.filter(history_date__lte = form_id.resignation_standalone.date_updated,
                                                            id = form_id.resignation_standalone.signer.id).values().latest()
        else:
            context['standalone_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_disable'):                  
            context['disable_signer'] = User.history.filter(history_date__lte = form_id.resignation_disable.date_updated,
                                                            id = form_id.resignation_disable.signer.id).values().latest()
        else:
            context['disable_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_primary'):                  
            context['primary_signer'] = User.history.filter(history_date__lte = form_id.resignation_primary.date_updated,
                                                            id = form_id.resignation_primary.signer.id).values().latest()
        else:
            context['primary_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_deletion'):                  
            context['deletion_signer'] = User.history.filter(history_date__lte = form_id.resignation_deletion.date_updated,
                                                            id = form_id.resignation_deletion.signer.id).values().latest()
        else:
            context['deletion_signer'] = 'not_signed'

        if hasattr(form_id, 'resignation_final'):                  
            context['final_signer'] = User.history.filter(history_date__lte = form_id.resignation_final.date_updated,
                                                            id = form_id.resignation_final.signer.id).values().latest()
        else:
            context['final_signer'] = 'not_signed'
                                                            



        pdf = render_to_pdf('blog/resignation_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')



