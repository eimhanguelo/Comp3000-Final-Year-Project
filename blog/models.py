from simple_history.utils import update_change_reason

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from users.models import *
from connectivity.models import *

from PIL import Image


from simple_history.models import HistoricalRecords


from multiselectfield import MultiSelectField


# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image
from django.utils import timezone
from multiselectfield import MultiSelectField
import datetime
from simple_history.models import HistoricalRecords
from simple_history.utils import update_change_reason

User = get_user_model()
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.utils import update_change_reason
from django.db import models
import datetime
from PIL import Image
from simple_history.models import HistoricalRecords

class Employee(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=30)
    emp_id = models.CharField(max_length=20)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True)
    emp_join_date = models.DateField(default=datetime.date.today)
    phone = models.CharField(max_length=15)
    ext = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    justification = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    # Add the historical records field
    history = HistoricalRecords()

    USER_CHOICES = (
        ('computer_login_access', 'Computer Login Access'),
        ('file_printer_share', 'File & Printer Sharing'),
    )
    user_activation = MultiSelectField(choices=USER_CHOICES, null=True, blank=True)

    MAIL_CHOICES = (
        ('ms_Outlook', 'Microsoft Outlook'),
        ('outgoing_permission', 'Outgoing Permission (Gmail, Other Company Mail)'),
        ('webmail', 'Webmail (Access from Chrome/Firefox through internet)'),
        ('Mail_access_from_phone', 'Mail Access from Mobile Phone'),
    )
    mail_activation = MultiSelectField(choices=MAIL_CHOICES, null=True, blank=True)

    GROUP_CHOICES = (
        ('dhaka_unit', 'SPL Dhaka Unit'),
        ('dhaka_unit_management', 'SPL Dhaka Unit Management'),
        ('dhaka_unit_managers', 'SPL Dhaka Unit Managers'),
    )
    group_access = MultiSelectField(choices=GROUP_CHOICES, null=True, blank=True)

    recommended_by = models.ForeignKey(User, related_name='recommended_by_emp', on_delete=models.SET_NULL, null=True)
    approved_hod = models.ForeignKey(User, related_name='approved_hod_emp', on_delete=models.SET_NULL, null=True)
    approved_hr = models.ManyToManyField(User, related_name='approved_hr_emp', verbose_name='Approved HR', blank=True)

    class Meta:
        verbose_name_plural = "Mail Account Creation FORM"

    def __str__(self):
        return f'HR-{self.id}/{self.author.id}/{self.author.profile.emp_id}'

    def get_absolute_url(self):
        return reverse('emp-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # Only resize the image and save the instance
        super().save(*args, **kwargs)  # Save instance first
        
        # Resize the image if needed
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

# Define a post-save signal for adding the change reason
@receiver(post_save, sender=Employee)
def update_employee_change_reason(sender, instance, created, **kwargs):
    if created:
        update_change_reason(instance, 'Employee Email form created')
    else:
        update_change_reason(instance, 'Employee Email form updated')


class EmployeeSign(models.Model):
    employee = models.OneToOneField(Employee, related_name='employee_sign', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.employee} {self.sign_type} by {self.signer}'

class EmployeeHOD(models.Model):
    employee = models.OneToOneField(Employee, related_name='employee_hod', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.employee} {self.sign_type} by {self.signer}'

class EmployeeHR(models.Model):
    employee = models.OneToOneField(Employee, related_name='employee_hr', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.employee} {self.sign_type} by {self.signer}'

class EmployeeIT(models.Model):
    employee = models.OneToOneField(Employee, related_name='employee_it', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    mail_id = models.EmailField(max_length = 100)
    mail_box = models.IntegerField(default=300)
    admin_comment = models.CharField(max_length=250)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.employee} signed by {self.admin}'

#==========================================Mail Modification==========================================


class Account(models.Model):
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    justification = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    USER_CHOICES = (
        ('computer_login_access', 'Computer Login Access'),
        ('file_printer_share', 'File & Printer Sharing'),
    )
    user_activation = MultiSelectField(max_length=100, choices=USER_CHOICES,null=True, blank=True)

    MAIL_CHOICES = (
        ('ms_Outlook', 'Microsoft Outlook'),
        ('outgoing_permission', 'Outgoing Permission (Gmail, Other Company Mail)'),
        ('webmail', 'Webmail (Access from Chrome/Firefox through internet)'),
        ('Mail_access_from_phone', 'Mail Access from Mobile Phone'),
    )
    mail_activation = MultiSelectField(max_length=100, choices=MAIL_CHOICES,null=True, blank=True)
    

    GROUP_CHOICES = (
        ('dhaka_unit', 'SPL Dhaka Unit'),
        ('dhaka_unit_management', 'SPL Dhaka Unit Management'),
        ('dhaka_unit_managers', 'SPL Dhaka Unit Managers'),
    )
    group_access = MultiSelectField(max_length=100, choices=GROUP_CHOICES, null=True, blank=True)

    recommended_by = models.ForeignKey(User, related_name='recommended_by', on_delete=models.SET_NULL, null=True)
    approved_hod = models.ForeignKey(User, related_name='approved_hod', on_delete=models.SET_NULL, null=True)
    approved_hr = models.ManyToManyField(User, related_name='approved_hr', verbose_name='Approved HR', blank=True)
    # Add the historical records field
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Account Modification FORM"

    def save(self, *args, **kwargs):
        if not self.pk:  
            hr_users = User.objects.filter(profile__is_hr=True)
            super().save(*args, **kwargs)
            self.approved_hr.set(hr_users)
        else:
            super().save(*args, **kwargs)


    def __str__(self):
        return f'MUAC-{self.id}/{self.author.id}/{self.author.profile.emp_id}'

    def get_absolute_url(self):
        return reverse('mail-detail', kwargs={'pk': self.pk})

# Define a post-save signal for adding the change reason
@receiver(post_save, sender=Account)
def update_employee_change_reason(sender, instance, created, **kwargs):
    if created:
        update_change_reason(instance, 'Email Modification Form created')
    else:
        update_change_reason(instance, 'Email Modification Form updated')

class AccountSign(models.Model):
    account = models.OneToOneField(Account, related_name='account_sign', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.account} {self.sign_type} by {self.signer}'

class AccountHOD(models.Model):
    account = models.OneToOneField(Account, related_name='account_hod', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.account} {self.sign_type} by {self.signer}'

class AccountHR(models.Model):
    account = models.OneToOneField(Account, related_name='account_hr', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.account} {self.sign_type} by {self.signer}'

class AccountIT(models.Model):
    account = models.OneToOneField(Account, related_name='account_it', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
   
    admin_comment = models.CharField(max_length=250)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.account} signed by {self.admin}'

class Resignation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    DATA_CONDITION = (
        ('transferred', 'Transferred'),
        ('destroyed', 'Destroyed'),
    )
    computer_data = models.CharField(max_length=30, choices=DATA_CONDITION, default='Transferred')
    computer_data_receiver = models.ForeignKey(User, related_name='computer_data_receiver', on_delete=models.SET_NULL, null=True)
    ARCHIVE_STATUS = (
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
    )
    email_archive = models.CharField(max_length=30, choices=ARCHIVE_STATUS, default='Completed')
    email_archive_receiver = models.ForeignKey(User, related_name='email_archive_receiver' ,on_delete=models.SET_NULL, null=True)

    computer_ip_address = models.ForeignKey(Lan, related_name='computer_ip_address', on_delete=models.SET_NULL, null=True)
    common_computer_ip = models.BooleanField()
    computer_ip_receiver = models.ForeignKey(User, related_name='computer_ip_receiver', on_delete=models.SET_NULL, null=True)

    ip_phone = models.CharField(max_length=10, null=True, blank=True)
    common_ip_phone = models.BooleanField()
    ip_phone_receiver = models.ForeignKey(User, related_name='ip_phone_receiver', on_delete=models.SET_NULL, null=True, blank=True)

    printer_owner = models.BooleanField()
    printer_receiever = models.ForeignKey(User, related_name='printer_receiver' ,on_delete=models.SET_NULL, null=True, blank=True)

    scanner_owner = models.BooleanField()
    scanner_receiever = models.ForeignKey(User, related_name='scanner_receiver', on_delete=models.SET_NULL, null=True, blank=True)

    internet_access = models.BooleanField()

    empower_id = models.CharField(max_length=50, null=True, blank=True)
    chromeleon_id = models.CharField(max_length=50, null=True, blank=True)

    eqms_id = models.CharField(max_length=50, null=True, blank=True)

    standalone_id = models.CharField(max_length=252, null=True, blank=True)

    recommended_hod = models.ForeignKey(User, related_name='recommended_hod_resignation', on_delete=models.SET_NULL, null=True)

    date_posted = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "IT Release FORM"

    def __str__(self):
        return f'RESG-{self.id}/{self.author.id}/{self.author.profile.emp_id}'

    def get_absolute_url(self):
        return reverse('resignation-detail', kwargs={'pk': self.pk})

class ResignationData(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_data', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'


class ResignationArchive(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_archive', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'

class ResignationIP(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_ip', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'


class ResignationPhone(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_phone', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'

class ResignationPrinter(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_printer', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'
    

class ResignationScanner(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_scanner', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'


class ResignationHOD(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_hod', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'

class ResignationInternet(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_internet', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'

class ResignationEmpower(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_empower', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'

class ResignationChromeleon(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_chromeleon', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'


class ResignationEqms(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_eqms', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'


class ResignationStandalone(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_standalone', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'

class ResignationDisable(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_disable', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'

class ResignationPrimary(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_primary', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'


class ResignationDeletion(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_deletion', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'


class ResignationFinal(models.Model):
    resignation = models.OneToOneField(Resignation, related_name='resignation_final', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.resignation} done by {self.signer}'


















