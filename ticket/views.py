from ast import Assign
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import engines
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from blog.views import ITUserMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
)
from .models import *
from .forms import *

from django.core.mail import send_mail, BadHeaderError, EmailMessage, EmailMultiAlternatives

from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages

from django.db.models import Q

from django.http import JsonResponse

from django.db.models.functions import window

from django.db.models import Subquery, OuterRef
from informatix.models import Roster


class EngineerTicketListView(LoginRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))

        context = {
            'tickets': Eticket.objects.all(),
            'total_tickets': Eticket.objects.all().count(),
            'total_resolved': Eticket.objects.filter(status='Solved').count(),   
            'unassigned_tickets': Eticket.objects.filter(status='Pending').count(),
            'total_all_pending': Eticket.objects.filter(status='Working').count(),
            'total_my_pending': Eticket.objects.filter(status='Working', ticket_engineer=user).count(),
  
        }
        return render(request, 'ticket/eticket_engineer.html', context)



class UserTicketListView(LoginRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))

        context = {
            
            'tickets': Eticket.objects.filter(ticket_raiser=user).exclude(status='Working'),

            'engineer_queue': Eticket.objects.filter(status='Working').annotate
                        (row_number=models.Window(
                            expression=window.RowNumber(),
                            partition_by=[models.F('ticket_engineer')],
                            order_by=[models.F('id').asc()],
                )).order_by('id')
                        }
        return render(request, 'ticket/eticket_users.html', context)

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Eticket

    def get_context_data(self, **kwargs):
        ticket = self.get_object()
        context = super(TicketDetailView, self).get_context_data(**kwargs)

        formatted_ticket_id = f'ETCKT-{ticket.pk}/{ticket.ticket_raiser.id}/{ticket.ticket_raiser.profile.emp_id}'

        context['formatted_ticket_id'] = formatted_ticket_id

        if hasattr(ticket, 'e_solve'):
            context['admin_history'] = ticket
        else:
            context['admin_history'] = 'not_signed'

        return context

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from .models import Eticket
from .forms import TicketCreationForm

from django.utils import timezone
import logging

# Initialize logger (if not done already)
logger = logging.getLogger(__name__)

class TicketCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Eticket
    form_class = TicketCreationForm
    success_message = 'E-Ticket is created and mail sent successfully ..!!'

    def form_valid(self, form):
        # Assign the ticket raiser to the current logged-in user
        form.instance.ticket_raiser = self.request.user

        # Proceed with form validation (saving the form)
        response = super().form_valid(form)

        # Retrieve the primary key of the created ticket and the ticket raiser
        pk = form.instance.pk
        raiser = form.instance.ticket_raiser

        # Generate the e-ticket link and ticket number
        eticket_link = f"{settings.WEB_HOST}/eticket/{pk}/"
        eticket_no = f'ETCKT-{pk}/{raiser.id}/{raiser.profile.emp_id}'
        try:
            # Fetch the active roster for the logged-in user
            active_roster = Roster.objects.get(is_active=True)
            form.instance.roster = active_roster  # Optionally associate the ticket with the roster
            supervisor = active_roster.supervisor  # Get the supervisor
            month = active_roster.month  # Get the month
        except Roster.DoesNotExist:
            # If no active roster is found, set defaults or handle as needed
            supervisor = None
            month = None
        # Prepare the context for the email template
        context = {
            'ticket_raiser_name': raiser.first_name,
            'problem_category': form.cleaned_data['problem_category'],
            'problem_description': form.cleaned_data['problem_description'],
            'link': eticket_link,
            'id': eticket_no,  # Use the ticket number format here
            'supervisor_name': supervisor.first_name if supervisor else 'N/A',  # Add supervisor name to context
            'month': month if month else 'N/A',  # Add month to context
        }

        # Render HTML and plain-text email messages
        html_message = render_to_string('ticket/mail_raise.html', context)
        plain_message = strip_tags(html_message)

        # Prepare the email message
        email_subject = f'E-Ticket Submission Confirmation: [ {eticket_no} ]'
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.request.user.email],
        )
        msg.attach_alternative(html_message, "text/html")

        # Send the email and handle potential exceptions
        try:
            msg.send()
        except Exception as e:
            # Log the error (you can also use Django's logging framework)
            print(f"Error sending email: {e}")

        # Log the audit trail (Ensure this is done only once)
        self.log_audit_trail(form.instance, self.request.user, 'CREATE')

        return response

    def log_audit_trail(self, ticket, user, action):
        """Log an audit trail entry for ticket creation."""
        try:
            # Stripping HTML tags from the problem description to store plain text
            clean_description = strip_tags(ticket.problem_description)

            # Create the audit trail record
            AuditTrail.objects.create(
                ticket=ticket,
                performed_by=user,  # Fix: should be performed_by instead of user
                action_type=action,  # Fix: use action_type instead of action
                performed_at=timezone.now(),  # Fix: use performed_at instead of timestamp
                details=f"Ticket created with ID: {ticket.id}, "
                         f"Problem Category: {ticket.problem_category}, "
                         f"Description: {clean_description}"  # Stripped HTML tags
            )
            logger.info(f"Audit trail logged for ticket creation: {ticket.id}")
        except Exception as e:
            logger.error(f"Error logging audit trail for ticket {ticket.id}: {e}")

    def get_success_url(self):
        # Redirect to the ticket detail page after successful creation
        return reverse('ticket-detail', kwargs={'pk': self.object.pk})



from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.views.generic import CreateView

class EAssignCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EAssign
    form_class = AssignForm
    success_message = 'E-Ticket is assigned and mail sent successfully ..!!'

    def form_valid(self, form):
        # Assign the current user as the assigner
        form.instance.assigner = self.request.user
        form.instance.eticket_id = self.kwargs['pk']

        # Retrieve the associated ticket (assign)
        assign = form.instance.eticket

        # Update the status and engineer assignment
        assign.status = 'Working'
        assign.ticket_engineer = form.cleaned_data['engineer']
        assign.save()

        engineer = form.cleaned_data['engineer']
        try:
            # Fetch the active roster for the logged-in user
            active_roster = Roster.objects.get(is_active=True)
            form.instance.roster = active_roster  # Optionally associate the ticket with the roster
            supervisor = active_roster.supervisor  # Get the supervisor
            month = active_roster.month  # Get the month
        except Roster.DoesNotExist:
            # If no active roster is found, set defaults or handle as needed
            supervisor = None
            month = None
        # ---------------------------- EMAIL PART -------------------------------
        context = {
            'ticket_raiser_name': assign.ticket_raiser.first_name,
            'ticket_raiser': assign.ticket_raiser,
            'engineer': engineer.first_name,
            'assign_type': form.instance.assign_type,
            'phone': engineer.profile.phone,
            'ext': engineer.profile.ext,
            'ticket_no': assign,  # Represents the ticket object, you may want to format it as a string (str(assign))
            'problem_category': assign.problem_category,
            'problem_description': assign.problem_description,
            'id': form.instance.eticket_id,
            'link': f"{settings.WEB_HOST}/eticket/{form.instance.eticket_id}/",
            'supervisor_name': supervisor.first_name if supervisor else 'N/A',  # Add supervisor name to context
            'month': month if month else 'N/A',  # Add month to context
        }

        # Render HTML and plain-text versions of the email
        html_message = render_to_string('ticket/mail_assign.html', context)
        plain_message = strip_tags(html_message)

        # Prepare the email message
        # email_subject = f'Assigning Ticket [ {assign} ]'
        email_subject = f'E-Ticket Assignment/Forward Notification: [ {assign} ]'
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[assign.ticket_raiser.email],
        )
        msg.attach_alternative(html_message, "text/html")

        # Send the email and handle potential exceptions
        try:
            msg.send()
        except Exception as e:
            # Log or print the error if email sending fails (consider using logging)
            print(f"Error sending email: {e}")

        
        # Log the audit trail after the action
        self.log_audit_trail(assign, self.request.user, 'ASSIGN')

        return super().form_valid(form)


    def log_audit_trail(self, ticket, user, action):
        """Log an audit trail entry for ticket assignment."""
        try:
            AuditTrail.objects.create(
                ticket=ticket,
                performed_by=user,
                action_type=action,
                performed_at=timezone.now(),
                details=f"Ticket assigned to {ticket.ticket_engineer} by {user}"
            )
        except Exception as e:
            # Log the error related to audit trail creation
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error logging audit trail for assignment of ticket {ticket.id}: {e}")

    def get_success_url(self, **kwargs):
    # Get the username of the currently logged-in user
        username = self.request.user.username
        return reverse('ticket-engineers', kwargs={'username': username})


from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.views.generic import CreateView

import logging
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import ESolve, AuditTrail

class ESolveCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ESolve
    fields = ['solve_type', 'note']
    success_message = 'E-Ticket is resolved and mail sent successfully ..!!'

    def form_valid(self, form):
        form.instance.solver = self.request.user
        form.instance.eticket_id = self.kwargs['pk']

        # ---------------------------- EMAIL PART -------------------------------
        solve = form.instance.eticket

        # Update ticket status to "Solved"
        solve.status = 'Solved'
        solve.save()

        engineer = form.instance.solver
        try:
            # Fetch the active roster for the logged-in user
            active_roster = Roster.objects.get(is_active=True)
            form.instance.roster = active_roster  # Optionally associate the ticket with the roster
            supervisor = active_roster.supervisor  # Get the supervisor
            month = active_roster.month  # Get the month
        except Roster.DoesNotExist:
            # If no active roster is found, set defaults or handle as needed
            supervisor = None
            month = None
        # Prepare the context for the email
        context = {
            'ticket_raiser_name': solve.ticket_raiser.first_name,
            'ticket_raiser': solve.ticket_raiser,
            'engineer': engineer.first_name,
            'solve_type': form.instance.solve_type,  # Correctly reference from the form instance
            'phone': engineer.profile.phone,
            'ext': engineer.profile.ext,
            'ticket_no': str(solve),  # Use the string representation of the solve ticket
            'problem_category': solve.problem_category,
            'problem_description': solve.problem_description,
            'id': form.instance.eticket_id,
            'link': f"{settings.WEB_HOST}/eticket/{form.instance.eticket_id}/",
            'note': form.instance.note,
            'supervisor_name': supervisor.first_name if supervisor else 'N/A',  # Add supervisor name to context
            'month': month if month else 'N/A',  # Add month to context
        }

        # Render HTML and plain-text versions of the email
        html_message = render_to_string('ticket/mail_solve.html', context)
        plain_message = strip_tags(html_message)

        # Prepare the email message
        email_subject = f'E-Ticket Solved/Closed Notification: [ {solve} ]'
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[solve.ticket_raiser.email],
        )

        msg.attach_alternative(html_message, "text/html")

        # Send the email and handle potential exceptions
        try:
            msg.send()
        except Exception as e:
            # Use proper logging instead of print statements
            logger = logging.getLogger(__name__)
            logger.error(f"Error sending email for ticket {solve.id}: {e}")

        # Log the audit trail after solving the ticket
        self.log_audit_trail(solve, self.request.user, 'RESOLVE', form.instance.solve_type, form.instance.note)

        return super().form_valid(form)

    def log_audit_trail(self, ticket, user, action, solve_type, note):
        """Log an audit trail entry for ticket resolution."""
        try:
            AuditTrail.objects.create(
                ticket=ticket,
                performed_by=user,
                action_type=action,
                performed_at=timezone.now(),
                details=f"Ticket resolved with type {solve_type} and note: {note} by {user}"
            )
        except Exception as e:
            # Log the error related to audit trail creation
            logger = logging.getLogger(__name__)
            logger.error(f"Error logging audit trail for resolution of ticket {ticket.id}: {e}")

    def get_success_url(self, **kwargs):
    # Get the username of the currently logged-in user
        username = self.request.user.username
        return reverse('ticket-engineers', kwargs={'username': username})



from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.views.generic import CreateView

import logging
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import EDiscussion, AuditTrail

class EDiscussionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EDiscussion
    fields = ['discussion']
    success_message = 'E-Ticket message has been successfully posted..!!'

    def form_valid(self, form):
        # Set the discusser (the current user) and eticket ID
        form.instance.discusser = self.request.user
        form.instance.eticket_id = self.kwargs['pk']

        # Call the parent class's form_valid method to save the form
        response = super().form_valid(form)

        # Get the associated ticket and executive engineer
        assign_ticket = form.instance.eticket
        ticket = assign_ticket  # No need for the extra query since assign_ticket is already the instance

        executive_engineer = ticket.ticket_engineer

        # Determine the sender and receiver based on who is interacting with the ticket
        if self.request.user == ticket.ticket_raiser:
            sender = ticket.ticket_raiser
            receiver = executive_engineer
        else:
            receiver = ticket.ticket_raiser
            sender = self.request.user

        # ---------------------------- EMAIL PART -------------------------------
        context = {
            'ticket_raiser_name': ticket.ticket_raiser.first_name,
            'receiver': receiver.first_name,
            'discussion': form.cleaned_data['discussion'],
            'sender': sender.first_name,
            'phone': sender.profile.phone,
            'ext': sender.profile.ext,
            'ticket_no': str(ticket),  # Ticket number as a string (you can use ticket.ticket_no if available)
            'id': form.instance.eticket_id,
            'link': f"{settings.WEB_HOST}/eticket/{form.instance.eticket_id}/"
        }

        # Render the email templates (HTML and plain text)
        html_message = render_to_string('ticket/mail_discuss.html', context)
        plain_message = strip_tags(html_message)

        # Prepare the email message
        email_subject = f'E-Ticket Discussion Message: [{ticket}]'
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[receiver.email],
            cc=[sender.email]  # CC the sender (the user who created the discussion)
        )
        msg.attach_alternative(html_message, "text/html")

        # Send the email and handle any potential exceptions
        try:
            msg.send()
        except Exception as e:
            # Log or print the error if email sending fails (consider using logging in production)
            print(f"Error sending email: {e}")

        # ------------------------ Log Audit Trail ---------------------------
        self.log_audit_trail(ticket, self.request.user, 'MESSAGE', form.cleaned_data['discussion'])

        return response

    def log_audit_trail(self, ticket, user, action, discussion_content):
        """Log an audit trail entry for a discussion/comment on the ticket."""
        try:
            AuditTrail.objects.create(
                ticket=ticket,
                performed_by=user,
                action_type=action,
                performed_at=timezone.now(),
                details=f"Message Sent: {discussion_content} by {user}"
            )
        except Exception as e:
            # Log the error related to audit trail creation
            logger = logging.getLogger(__name__)
            logger.error(f"Error logging audit trail for ticket {ticket.id}: {e}")

    def get_success_url(self, **kwargs):
    # Get the username of the currently logged-in user
        username = self.request.user.username
        return reverse('ticket-engineers', kwargs={'username': username})


import logging
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import EInternal, AuditTrail

class EInternalCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EInternal
    fields = ['discussion']
    success_message = 'E-Ticket status updated successfully!'

    def form_valid(self, form):
        form.instance.admin = self.request.user
        form.instance.eticket_id = self.kwargs['pk']

        # Call the parent class's form_valid method to save the form
        response = super().form_valid(form)

        # Get the associated ticket from the form instance
        ticket = form.instance.eticket

        # Log the audit trail for this internal discussion
        self.log_audit_trail(ticket, self.request.user, 'COMMENT', form.cleaned_data['discussion'])

        return response

    def log_audit_trail(self, ticket, user, action, discussion_content):
        """Log an audit trail entry for updating the ticket's internal status or discussion."""
        try:
            AuditTrail.objects.create(
                ticket=ticket,
                performed_by=user,
                action_type=action,
                performed_at=timezone.now(),
                details=f"Internal discussion/Update: {discussion_content} by {user}"
            )
        except Exception as e:
            # Log the error related to audit trail creation
            logger = logging.getLogger(__name__)
            logger.error(f"Error logging audit trail for ticket {ticket.id}: {e}")

    def get_success_url(self, **kwargs):
    # Get the username of the currently logged-in user
        username = self.request.user.username
        return reverse('ticket-engineers', kwargs={'username': username})


# Create your views here.
class PendingTicketListView(LoginRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):

        context = {
            'tickets': Eticket.objects.filter(status='Pending'),
            'pending_tickets': Eticket.objects.filter(status='Pending').count(),

        }
        return render(request, 'ticket/pending_ticket.html', context)

@login_required
def assign_engineer(request, pk):
    eticket = Eticket.objects.get(pk=pk)
    assigns = EAssign.objects.filter(eticket=eticket)
    form = AssignForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            assign = form.save(commit=False)
            assign.eticket = eticket
            assign.assigner = request.user            
            assign.save()

            eticket.status = 'Working'
            eticket.ticket_engineer = form.cleaned_data['engineer']
            eticket.save()

            return redirect("detail-assign", pk=assign.id)
        else:
            return render(request, "ticket/partials/assign_form.html", {
                "form": form
            })

    context = {
        'form': form,
        'eticket': eticket,
        "assigns": assigns
    }
    return render(request, 'ticket/pending_ticket.html', context)


@login_required
def assign_form(request):
    context={
        "form": AssignForm()
    }
    return render(request, "ticket/partials/assign_form.html", context)

@login_required
def detail_assign(request, pk):
    assign = EAssign.objects.get(pk=pk)
    context = {
        "assign": assign
    }
    return render(request, "ticket/partials/assign_detail.html", context)
