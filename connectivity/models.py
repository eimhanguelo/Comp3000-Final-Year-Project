from pyexpat import model
from xml.etree.ElementTree import Comment
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from simple_history.models import HistoricalRecords

from multiselectfield import MultiSelectField
from ckeditor.fields import RichTextField
from users.models import *
from hardware.models import *
# Create your models here.


class OS(models.Model):
    name = models.CharField(max_length=40, unique=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']  # Orders by id in ascending order by default

class Switch(models.Model):
    name = models.CharField(max_length=40, unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']  # Orders by id in ascending order by default

class CentralProcessingUnit(models.Model):
    name = models.CharField(max_length=40, unique=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']  # Orders by id in ascending order by default

class PrinterModel(models.Model):
    name = models.CharField(max_length=40, unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']  # Orders by id in ascending order by default

class ScannerModel(models.Model):
    name = models.CharField(max_length=40, unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']  # Orders by id in ascending order by default


class Lan(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(unique=True)
    computer_name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    os = models.ForeignKey(OS, on_delete=models.SET_NULL, null=True)
    vlan = models.IntegerField(default=0)
    switch_name = models.ForeignKey(Switch, on_delete=models.SET_NULL, null=True)
    switch_port = models.IntegerField(default=0, blank=True, null=True)
    cable_tag = models.CharField(max_length=20, default='N/A', blank=True, null=True)
    cpu_model = models.ForeignKey(CentralProcessingUnit, on_delete=models.SET_NULL, null=True)
    printer_model = models.ForeignKey(PrinterModel, on_delete=models.SET_NULL, null=True, blank=True)
    scanner_model = models.ForeignKey(ScannerModel, on_delete=models.SET_NULL, null=True, blank=True)
    ip_used = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=timezone.now)

    used_by = models.ForeignKey(User, related_name='lan_user', on_delete=models.SET_NULL, 
                                null=True, blank=True, verbose_name='Lan User')

    instrument_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Instrument Name')
    instrument_id = models.CharField(max_length=30, null=True, blank=True, verbose_name='Instrument ID')

    location = models.ForeignKey(Location, on_delete=models.SET_NULL, 
                                null=True, blank=True, verbose_name='Lan Location')
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL,
                             null=True, blank=True, verbose_name='Lan Floor')

    # Add the historical records field
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Network Inventory Section"

    def __str__(self):
        return self.ip_address

    def get_absolute_url(self):
        return reverse('lan-detail', kwargs={'pk': self.pk})

class LanRequest(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    justification = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    recommended_hod = models.ForeignKey(User, related_name='recommended_hod', on_delete=models.SET_NULL, null=True)
    # Add the historical records field
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Computer LAN Connectivity"

    def __str__(self):
        return f'LCRF-{self.id}/{self.author.id}/{self.author.profile.emp_id}'

    def get_absolute_url(self):
        return reverse('lan1-detail', kwargs={'pk': self.pk})

# Define a post-save signal for adding the change reason
@receiver(post_save, sender=LanRequest)
def update_LanRequest_change_reason(sender, instance, created, **kwargs):
    if created:
        update_change_reason(instance, 'LanRequest created')
    else:
        update_change_reason(instance, 'LanRequest updated')

        
class LanRequestSign(models.Model):
    lanrequest = models.OneToOneField(LanRequest, related_name='lanrequest_sign', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.lanrequest} {self.sign_type} by {self.signer}'


class LanRequestIT(models.Model):
    lanrequest = models.OneToOneField(LanRequest, related_name='lanrequest_it', on_delete=models.CASCADE)
    required_ip_address = models.ForeignKey(Lan, related_name='lanrequest_ip', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.lanrequest} filled up by {self.admin}'


#-------------------------------------------------Lan Transfer Form-----------------------------------------------------

class LanTransfer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    current_ip_address = models.ForeignKey(Lan, related_name='lantransfer_ip', on_delete=models.CASCADE)
    transferee_location_old_ip_address = models.ForeignKey(Lan, related_name='old_lan_transfers', on_delete=models.CASCADE, null=True,blank=True)
    new_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    new_floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True)
    new_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    transfer_list = models.ManyToManyField(Product, blank=False)
    purpose_of_transfer = models.TextField()
    recommended_hod = models.ForeignKey(User, related_name='recommended_hod_lt', on_delete=models.SET_NULL, null=True)
    recommended_hr = models.ManyToManyField(User, related_name='recommended_hr_lt', verbose_name='Approved HR', blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Computer LAN Transfer"

    def __str__(self):
        return f'LCTF-{self.id}/{self.author.id}/{self.author.profile.emp_id}'

    def get_absolute_url(self):
        return reverse('lan2-detail', kwargs={'pk': self.pk})

    def get_filtered_transfer_list(self):
        """
        Return only the Products where transfer_list_item is True
        """
        return self.transfer_list.filter(transfer_list_item=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.pk:  
            hr_users = User.objects.filter(profile__is_hr=True)
            self.recommended_hr.set(hr_users)

# Define a post-save signal for adding the change reason
@receiver(post_save, sender=LanTransfer)
def update_LanTransfer_change_reason(sender, instance, created, **kwargs):
    if created:
        update_change_reason(instance, 'LanTransfer created')
    else:
        update_change_reason(instance, 'LanTransfer updated')

class LanTransferHOD(models.Model):
    lantransfer = models.OneToOneField(LanTransfer, related_name='lantransfer_hod', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=15, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.lantransfer} {self.sign_type} by {self.signer}'

class LanTransferHR(models.Model):
    lantransfer = models.OneToOneField(LanTransfer, related_name='lantransfer_hr', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=15, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.lantransfer} {self.sign_type} by {self.signer}'

class LanTransferIT(models.Model):
    lantransfer = models.OneToOneField(LanTransfer, related_name='lantransfer_it', on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.lantransfer} filled up by {self.admin}'


#------------------------------------------Request for Instrument LAN Connectivity-------------------------------------

class LanInstrument(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    instrument_name = models.CharField(max_length=50)
    instrument_id = models.CharField(max_length=30)
    justification = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    recommended_hod = models.ForeignKey(User, related_name='recommended_hod_li', on_delete=models.SET_NULL, null=True)
    # Add the historical records field
    history = HistoricalRecords()
    class Meta:
        verbose_name_plural = "Instrument LAN Connectivity"

    def __str__(self):
        return f'RILC-{self.id}/{self.author.id}/{self.author.profile.emp_id}'

    def get_absolute_url(self):
        return reverse('lan3-detail', kwargs={'pk': self.pk})

# Define a post-save signal for adding the change reason
@receiver(post_save, sender=LanInstrument)
def update_LanInstrument_change_reason(sender, instance, created, **kwargs):
    if created:
        update_change_reason(instance, 'LanInstrument created')
    else:
        update_change_reason(instance, 'LanInstrument updated')

class LanInstrumentSign(models.Model):
    laninstrument = models.OneToOneField(LanInstrument, related_name='laninstrument_sign', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=15, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.laninstrument} {self.sign_type} by {self.signer}'

class LanInstrumentIT(models.Model):
    laninstrument = models.OneToOneField(LanInstrument, related_name='laninstrument_it', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    required_ip_address = models.ForeignKey(Lan, related_name='laninstrument_ip', on_delete=models.CASCADE)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.laninstrument} signed by {self.admin}'

#-------------------------------------------------LanTransfer Instrument Form-----------------------------------------------------
class LanTransferInstrument(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    current_ip_address = models.ForeignKey(Lan, related_name='lantransferinstrument_ip', on_delete=models.CASCADE)
    current_location = models.ForeignKey(Location, related_name='lantransferinstrument_current_location', on_delete=models.SET_NULL, null=True)
    current_floor = models.ForeignKey(Floor, related_name='lantransferinstrument_current_floor', on_delete=models.SET_NULL, null=True)
    current_department = models.ForeignKey(Department, related_name='lantransferinstrument_current_department', on_delete=models.SET_NULL, null=True, blank=True)
    new_location = models.ForeignKey(Location, related_name='lantransferinstrument_new_location', on_delete=models.SET_NULL, null=True)
    new_floor = models.ForeignKey(Floor, related_name='lantransferinstrument_new_floor', on_delete=models.SET_NULL, null=True)
    new_department = models.ForeignKey(Department, related_name='lantransferinstrument_new_department', on_delete=models.SET_NULL, null=True, blank=True)
    contact_person = models.ForeignKey(User, related_name='lantransferinstrument_contact', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='lantransferinstrument contact')
    purpose_of_transfer = models.TextField()
    recommended_hod = models.ForeignKey(User, related_name='lantransferinstrument_hod', on_delete=models.SET_NULL, null=True)
    recommended_hr = models.ManyToManyField(User, related_name='lantransferinstrument_hr', verbose_name='Approved HR', blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    class Meta:
        verbose_name_plural = "Instrument LAN Transfer"

    def __str__(self):
        return f'ILCT-{self.id}/{self.author.id}/{self.author.profile.emp_id}'
    
    def get_absolute_url(self):
        return reverse('lantransferinstrument-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the instance first to generate a primary key
        if not self.recommended_hr.exists():  # Only set recommended HR users if it's empty
            hr_users = User.objects.filter(profile__is_hr=True)
            self.recommended_hr.set(hr_users)

# Define a post-save signal for adding the change reason
@receiver(post_save, sender=LanTransferInstrument)
def update_LanTransferInstrument_change_reason(sender, instance, created, **kwargs):
    if created:
        update_change_reason(instance, 'LanTransferInstrument created')
    else:
        update_change_reason(instance, 'LanTransferInstrument updated')


class LanTransferInstrumentHOD(models.Model):
    lantransfer = models.OneToOneField(LanTransferInstrument, related_name='lantransfer_hod', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=15, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.lantransfer} {self.sign_type} by {self.signer}'


class LanTransferInstrumentHR(models.Model):
    lantransfer = models.OneToOneField(LanTransferInstrument, related_name='lantransfer_hr', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed'),
    )
    sign_type = models.CharField(max_length=15, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.lantransfer} {self.sign_type} by {self.signer}'



class LanTransferInstrumentIT(models.Model):
    lantransfer = models.OneToOneField('LanTransferInstrument', related_name='laninstrumenttransfer_it', on_delete=models.CASCADE,blank=True)
    required_ip_address = models.ForeignKey('Lan', related_name='lan_ip', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=250, null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    date_signed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.lantransfer} filled up by {self.admin}'

#----------------------------------------------Internet Access Activation Form------------------------------------------
class Internet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    justification = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    recommended_hod = models.ForeignKey(User, related_name='recommended_hod_ia', on_delete=models.SET_NULL, null=True)
    recommended_hr = models.ForeignKey(User, related_name='recommended_hr_ia', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Internet Activation FORM"

    def __str__(self):
        return f'IAAF-{self.id}/{self.author.id}/{self.author.profile.emp_id}'

    def get_absolute_url(self):
        return reverse('internet-detail', kwargs={'pk': self.pk})

class InternetHOD(models.Model):
    internet = models.OneToOneField(Internet, related_name='internet_hod', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null = True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.internet}--{self.sign_type}--{self.signer}'

class InternetHR(models.Model):
    internet = models.OneToOneField(Internet, related_name='internet_hr', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null = True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.internet}--{self.sign_type}--{self.signer}'

class InternetIT(models.Model):
    internet = models.OneToOneField(Internet, related_name='internet_it', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250, null = True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.internet} signed by {self.admin}'


#----------------------------------------------------Permission---------------------------------------------------------
class Permission(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    computer_name = models.CharField(max_length=30)
    ip_address = models.GenericIPAddressField()
    PERMISSION_TYPES = (
        ('administrative_permission', 'Administrative Permission (Computer Login with Admin)'),
        ('usb_access_permission', 'USB Access Permission (To get access Pendrive and Storage Devices)'),
    )
    permission_type = MultiSelectField(max_length=100, choices=PERMISSION_TYPES)
    justification = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    recommended_hod = models.ForeignKey(User, related_name='recommended_hod_permission', on_delete=models.SET_NULL, null=True)
    recommended_hr = models.ForeignKey(User, related_name='recommended_hr_permission', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "USB Permission FORM"

    def __str__(self):
        return f'UAAP-{self.id}/{self.author.id}/{self.author.profile.emp_id}'

    def get_absolute_url(self):
        return reverse('permission-detail', kwargs={'pk': self.pk})

class PermissionHOD(models.Model):
    permission = models.OneToOneField(Permission, related_name='permission_hod', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('agreed', 'Agreed'),
        ('disagreed', 'Disagreed')
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null = True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.permission}--{self.sign_type}--{self.signer}'


class PermissionHR(models.Model):
    permission = models.OneToOneField(Permission, related_name='permission_hr', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null = True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.permission}--{self.sign_type}--{self.signer}'

class PermissionIT(models.Model):
    permission = models.OneToOneField(Permission, related_name='permission_it', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250, null = True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.permission} signed by {self.admin}'

#------------------------------------------------------Filer Server Access-----------------------------------------------------------------

class FileAccess(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    other_dept_head = models.ForeignKey(User, related_name='recommended_hod_other', on_delete=models.SET_NULL, null=True, blank=True)
    recommended_by = models.ForeignKey(User, related_name='recommended_by_file', on_delete=models.SET_NULL, null=True)
    recommended_hod = models.ForeignKey(User, related_name='recommended_hod_file', on_delete=models.SET_NULL, null=True)
    revoke_access = models.TextField(null=True, blank=True)
    # Add the historical records field
    history = HistoricalRecords()
    class Meta:
        verbose_name_plural = "File Server Access"

    def __str__(self):
        return f'FSAF-{self.id}/{self.author.id}/{self.author.profile.emp_id}'

    def get_absolute_url(self):
        return reverse('filelink-create', kwargs={'pk': self.pk})

# Define a post-save signal for adding the change reason
@receiver(post_save, sender=FileAccess)
def update_FileAccess_change_reason(sender, instance, created, **kwargs):
    if created:
        update_change_reason(instance, 'FileAccess created')
    else:
        update_change_reason(instance, 'FileAccess updated')


class FileLink(models.Model):
    link_name = models.CharField(max_length=200)
    PERMISSION_TYPES = (
        ('Modify', 'Modify'),
        ('Read-Only', 'Read-Only'),
    )
    permission_type = models.CharField(max_length=10, choices=PERMISSION_TYPES)
    LOCATION_DEPT = (
        ('other', 'Other Dept.'),
        ('self', 'Self Dept.'),
    )
    location = models.CharField(max_length=10, choices=LOCATION_DEPT)
    fileaccess = models.ForeignKey(FileAccess, related_name='file_link', on_delete=models.CASCADE)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.fileaccess}--link_{self.id}'

class FileAccessOtherHOD(models.Model):
    fileaccess = models.OneToOneField(FileAccess, related_name='fileaccess_other_hod', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.fileaccess}--{self.sign_type}--{self.signer}'

class FileAccessSign(models.Model):
    fileaccess = models.OneToOneField(FileAccess, related_name='fileaccess_sign', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.fileaccess}--{self.sign_type}--{self.signer}'

class FileAccessHOD(models.Model):
    fileaccess = models.OneToOneField(FileAccess, related_name='fileaccess_hod', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.fileaccess}--{self.sign_type}--{self.signer}'


class FileAccessIT(models.Model):
    fileaccess = models.OneToOneField(FileAccess, related_name='fileaccess_it', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # Add the historical records field
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.fileaccess}--Sign By--{self.admin}'





