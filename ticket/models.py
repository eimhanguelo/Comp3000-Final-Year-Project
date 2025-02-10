from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from multiselectfield import MultiSelectField
from ckeditor.fields import RichTextField
# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from django.db.models.signals import post_save
from simple_history.utils import update_change_reason

class AuditTrail(models.Model):
    ACTION_TYPES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('ASSIGN', 'Assign'),
        ('RESOLVE', 'Resolve'),
        ('COMMENT', 'Comment'),
         ('MESSAGE', 'Message'),
    ]
    
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    ticket = models.ForeignKey('Eticket', on_delete=models.CASCADE, related_name='audit_logs')
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    performed_at = models.DateTimeField(default=now)
    details = models.TextField(blank=True, null=True)  # Store additional details like changes made.
    
    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.action_type} by {self.performed_by} on {self.ticket} at {self.performed_at}"

# Create your models here.

class ProblemCategory(models.Model):
    problem_name = models.CharField(max_length=100)

    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return self.problem_name


import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime
from django.utils.formats import date_format

# Custom file size validation
def validate_file_size(value):
    file_size = value.size
    limit_mb = 100  # Set the size limit in MB (for example, 5MB)
    if file_size > limit_mb * 1024 * 1024:  # Convert MB to bytes
        raise ValidationError(f"File size should not exceed {limit_mb}MB.")

# Custom upload path function for file attachments with a unique filename
from django.utils import timezone
def eticket_attachment_upload_path(instance, filename):
    # Ensure the datetime is aware
    date_raised = instance.date_raised
    if timezone.is_naive(date_raised):
        date_raised = timezone.make_aware(date_raised)
    
    # Convert to local time and format the date
    formatted_date = localtime(date_raised).strftime('%Y-%m-%d_%H-%M-%S')  # Format as 'YYYY-MM-DD_HH-MM-SS'
    
    # Construct the unique filename using ticket ID, ticket_raiser, date_raised, and the original filename
    unique_filename = f"ETKT-{instance.ticket_raiser}_{formatted_date}_{filename}"
    
    # Return the complete path inside 'Eticket_Attachment' folder
    return os.path.join('Eticket_Attachment', str(instance.ticket_raiser), unique_filename)

from django.db import models
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.utils import update_change_reason
from django.urls import reverse

from simple_history.models import HistoricalRecords
from django.db import models

from django.db import models
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.utils import update_change_reason
from django.contrib.auth.models import User
from django.urls import reverse


# Eticket Model
class Eticket(models.Model):
    ticket_raiser = models.ForeignKey(User, related_name='ticket_raiser', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    reference_form = models.CharField(max_length=30, null=True, blank=True)
    problem_category = models.ForeignKey('ProblemCategory', on_delete=models.SET_NULL, null=True)
    problem_description = RichTextField(null=False, blank=False, default="")  # Adding a default value
    status = models.CharField(max_length=50, default='Pending')
    ticket_engineer = models.ForeignKey(User, related_name='ticket_engineer',
                    on_delete=models.SET_NULL, blank=True, null=True)
    date_raised = models.DateTimeField(auto_now_add=True)
    form_link = models.URLField(null=True, blank=True)
    created_via = models.CharField(max_length=50, default='MANUAL')

    # Historical records tracking
    history = HistoricalRecords()

    # New file field for eticket attachment
    eticket_attachment = models.FileField(
        upload_to='eticket_attachments/',  # Specify your path here
        null=True,
        blank=True,
        verbose_name='Eticket Attachment',
        validators=[validate_file_size]  # Custom validator to check file size
    )

    def __str__(self):
        emp_id = getattr(self.ticket_raiser.profile, 'emp_id', 'Unknown')
        return f'ETCKT-{self.id}/{self.ticket_raiser.id}/{emp_id}'

    def get_absolute_url(self):
        return reverse('ticket-detail', kwargs={'pk': self.pk})
        

class EAssign(models.Model):
    eticket = models.ForeignKey(Eticket, related_name='e_assign', on_delete=models.CASCADE)
    assigner = models.ForeignKey(User, related_name='assigner', on_delete=models.CASCADE)
    engineer = models.ForeignKey(User, related_name='engineer', on_delete=models.CASCADE)
    ASSIGN_TYPE = (
        ('assigned', 'Assigned'),
        ('forwarding', 'Forwarding')
    )
    assign_type = models.CharField(max_length=50, choices=ASSIGN_TYPE, default='Assigned')
    date_assigned = models.DateTimeField(auto_now_add=timezone.now)

    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.eticket} {self.assign_type} to model no : {self.id}--{self.engineer}'


class ESolve(models.Model):
    eticket = models.OneToOneField(Eticket, related_name='e_solve', on_delete=models.CASCADE)
    solver = models.ForeignKey(User, related_name='solver', on_delete=models.CASCADE)
    SOLVE_TYPE = (
        ('solved', 'Solved'),
        ('closed', 'Closed')
    )
    solve_type = models.CharField(max_length=20, choices=SOLVE_TYPE, default='Solved')
    note = models.TextField(null=True, blank=True)
    # problem_solution = models.TextField(default='done')
    date_solved = models.DateTimeField(auto_now_add=timezone.now)
    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.solver}---{self.solve_type}--{self.eticket}'

class EDiscussion(models.Model):
    eticket = models.ForeignKey(Eticket, related_name='e_discuss', on_delete=models.CASCADE)
    discusser = models.ForeignKey(User, related_name='discusser', on_delete=models.CASCADE)
    discussion = models.TextField()
    date_discussed = models.DateTimeField(auto_now_add=timezone.now)
    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.discusser}-(self.id)--{self.eticket}'

class EInternal(models.Model):
    eticket = models.ForeignKey(Eticket, related_name='e_internal', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, related_name='e_admin', on_delete=models.CASCADE)
    discussion = models.TextField()
    date_discussed = models.DateTimeField(auto_now_add=timezone.now)
    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.admin}-(self.id)--{self.eticket}'