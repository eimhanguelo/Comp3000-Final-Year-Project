from codecs import charmap_build
from operator import mod
from tabnanny import verbose
# from turtle import position
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from simple_history.models import HistoricalRecords

from users.models import *
from connectivity.models import *

from django.core.validators import MinValueValidator
# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from users.models import Profile 
from datetime import datetime
import os
from simple_history.models import HistoricalRecords

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    has_asset_no = models.BooleanField(default=False)
    transfer_list_item = models.BooleanField(default=False)

    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Model')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class CostCenter(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return self.name

def validate_file_size(value):
    max_size = 100 * 1024 * 1024  # 100 MB in bytes
    if value.size > max_size:
        raise ValidationError(f"File size cannot exceed 100 MB. Current size: {value.size / (1024 * 1024):.2f} MB.")

def requisition_attachment_upload_path(instance, filename):
    # Extract the original file extension
    file_extension = os.path.splitext(filename)[1]
    # Get the current timestamp
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Generate a unique filename using requisition_no and timestamp
    unique_filename = f"Requisition_{instance.requisition_no}_{current_time}_attachment{file_extension}"
    # Return the full path
    return os.path.join('Requisition_attachment', unique_filename)

class Requisition(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    REQUISITION_TYPE = (
        ('new', 'New'),
        ('repair', 'Repair'),
    )
    
    requisition_type = models.CharField(max_length=50, choices=REQUISITION_TYPE, verbose_name='Requisition Type')
    requisition_no = models.CharField(max_length=100, verbose_name='Requisition No')
    cost_center = models.ForeignKey(CostCenter, on_delete=models.SET_NULL, null=True, verbose_name='Cost Center')
    
    recommended_by = models.ForeignKey(User, related_name='recommended_by_requisitions', on_delete=models.SET_NULL, null=True, verbose_name='Recommended By')
    recommended_hod = models.ForeignKey(User, related_name='recommended_hod_requisitions', on_delete=models.SET_NULL, null=True, verbose_name='Recommended HOD')

    recommended_hr = models.ManyToManyField(User, related_name='recommended_hr_requisitions', verbose_name='Recommended HR (if Required)', blank=True)
    recommended_accountant = models.ManyToManyField(User, related_name='recommended_accountant_requisitions', verbose_name='Recommended Accountant (if Required)', blank=True)
    recommended_verifier_it = models.ManyToManyField(User, related_name='recommended_verifier_it_requisitions', verbose_name='Recommended Verifier of IT', blank=True)
    recommended_hod_it = models.ManyToManyField(User, related_name='recommended_hod_it_requisitions', verbose_name='Recommended HODs of IT', blank=True)

    # Add the historical records field
    history = HistoricalRecords()

    requisition_attachment = models.FileField(
        upload_to=requisition_attachment_upload_path,
        null=True,
        blank=True,
        verbose_name='Requisition Attachment',
        validators=[validate_file_size]  # Add custom validator for file size limit
    )

    class Meta:
        verbose_name_plural = "IT Requisition Forms"

    def __str__(self):
        return f'RQSN-{self.id}/{self.author.id}/{self.author.profile.emp_id}'

    def get_absolute_url(self):
        return reverse('prod-create', kwargs={'pk': self.pk})


    def save(self, *args, **kwargs):
        if not self.requisition_no:  # Only generate requisition_no if it's not already set
            # Ensure the author has a profile with department and location
            if not self.author.profile:
                raise ValidationError("Author must have a profile.")
            profile = self.author.profile

            # Get department and location from the author's profile
            department = profile.department
            location = profile.location

            # Ensure department and location are available
            if not department or not location:
                raise ValidationError("Author's profile must have both a department and location.")

            # Clean up department and location names (strip spaces and remove periods)
            department_name = department.name.strip().replace('.', '')
            location_name = location.name.strip().replace('.', '')

            # Use the last two digits of the current year
            current_year = datetime.now().year
            year_suffix = str(current_year)[-2:]  # e.g., '24' for 2024

            # Find all requisitions for this department-location combination in the current year, ending with year_suffix
            existing_requisitions = Requisition.objects.filter(
                requisition_no__startswith=f"{department_name}/{location_name}",  # Filter by department and location
                requisition_no__endswith=f"/{year_suffix}"  # Filter by year suffix
            ).order_by('date_posted')

            # Determine the next requisition number for the department-location
            if not existing_requisitions:
                new_number = 1  # If no existing requisitions, start from 1
            else:
                last_requisition = existing_requisitions.last()  # Get the last requisition in the list
                # Extract the last number from requisition_no (e.g., "HR/NYC/001/24")
                last_number = int(last_requisition.requisition_no.split('/')[2])  # Get the number part
                new_number = last_number + 1  # Increment the number

            # Format the new_number to be 3 digits with leading zeros (e.g., 001, 002, ...)
            formatted_number = f"{new_number:03}"

            # Generate the requisition_no using department, location, and year suffix
            self.requisition_no = f"{department_name}/{location_name}/{formatted_number}/{year_suffix}"

        # Save the instance (either with the newly generated requisition_no or an existing one)
        super().save(*args, **kwargs)


        # Populate many-to-many fields after saving
        if self.pk:  
            hr_users = User.objects.filter(profile__is_hr=True)
            self.recommended_hr.set(hr_users)

            accountant_users = User.objects.filter(profile__is_accountant=True)
            self.recommended_accountant.set(accountant_users)

            verifier_it_users = User.objects.filter(profile__is_verifier_it=True)
            self.recommended_verifier_it.set(verifier_it_users)

            hod_it_users = User.objects.filter(profile__is_hod_it=True)
            self.recommended_hod_it.set(hod_it_users)

            
    def has_product_with_asset_no(self):
        for item in self.requisition_inventory.all():
            # print(item.product.has_asset_no)  # Debugging line
            if item.product.has_asset_no:
                return True
        return False

    def is_recommended_by_hod_same(self):
        """
        Returns True if 'recommended_by' and 'recommended_hod' are the same user,
        otherwise returns False.
        """
        if self.recommended_by == self.recommended_hod:
            return True
        else:
            return False

    # def is_HR_Super(self):
    #     if self.recommended_hod and self.recommended_hod.username == "HR_Super":
    #         return True
    #     else:
    #         return False

    def is_HR_Super(self):
        if self.recommended_hod and self.recommended_hod.username in {"HR_Super", "HR_ADMIN"}:
            return True
        else:
            return False

from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.utils import update_change_reason
from .models import Requisition

# Flag to prevent recursion
save_in_progress = False

@receiver(post_save, sender=Requisition)
def update_requisition_change_reason(sender, instance, created, **kwargs):

    # Set the change reason based on whether the instance is created or updated
    if created:
        update_change_reason(instance, 'Requisition form created')
    else:
        update_change_reason(instance, 'Requisition form updated')



class RequisitionAsset(models.Model):
    requisition = models.OneToOneField(Requisition, related_name='requisition_asset', on_delete=models.CASCADE)
    asset_provider = models.ForeignKey(User, on_delete=models.CASCADE)
    asset_no = models.CharField(max_length=100, unique=True, verbose_name='Asset No')
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.requisition} Asset Provided by {self.asset_provider}'

class RequisitionSign(models.Model):
    requisition = models.OneToOneField(Requisition, related_name='requisition_sign', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)

    # Add the historical records field
    history = HistoricalRecords()
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.requisition} {self.sign_type} by {self.signer}'

class RequisitionHOD(models.Model):
    requisition = models.OneToOneField(Requisition, related_name='requisition_hod', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)

    # Add the historical records field
    history = HistoricalRecords()
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.requisition} {self.sign_type} by {self.signer}'

class RequisitionHR(models.Model):
    requisition = models.OneToOneField(Requisition, related_name='requisition_hr', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Add the historical records field
    history = HistoricalRecords()   
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.requisition} {self.sign_type} by {self.signer}'

class RequisitionACC(models.Model):
    requisition = models.OneToOneField(Requisition, related_name='requisition_accountant', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)

    # Add the historical records field
    history = HistoricalRecords()
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    new_asset_no = models.CharField(max_length=100, verbose_name='New Asset No', default='')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.requisition} {self.sign_type} by {self.signer}'

class RequisitionVERIFY(models.Model):
    requisition = models.OneToOneField(Requisition, related_name='requisition_verify', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)

    # Add the historical records field
    history = HistoricalRecords()
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    verified_by_it = models.BooleanField(default=False)
    date_signed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.requisition} {self.sign_type} by {self.signer}'

class RequisitionHODIT(models.Model):
    requisition = models.OneToOneField(Requisition, related_name='requisition_hod_it', on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)

    # Add the historical records field
    history = HistoricalRecords()
    
    SIGN_CHOICES = (
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    )
    
    sign_type = models.CharField(max_length=50, choices=SIGN_CHOICES, default='Agreed')
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.requisition} {self.sign_type} by {self.signer}'

class RequisitionIT(models.Model):
    requisition = models.OneToOneField(Requisition, related_name='requisition_it', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250, null=True, blank=True)
    date_signed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    # Add the historical records field
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.requisition} Signed by {self.admin}'



def user_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'chalan_{0}/{1}'.format(instance.chalan, filename)

class QuantityUnit(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name



class Inventory(models.Model):
    requisition = models.ForeignKey(Requisition, related_name='requisition_inventory', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, related_name='inventory_product', on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_type = models.ForeignKey(QuantityUnit, on_delete=models.SET_NULL, null=True, verbose_name='Unit Type')
    details = models.CharField(max_length=254, null=True, blank=True, verbose_name='Product Details')
    remarks = models.CharField(max_length=254, null=True, blank=True)
    date_of_last_issue = models.DateField(null=True, blank=True, verbose_name='Date of Last Issue')


    PRODUCT_CONDITION= (
        ('Requisition Raised', 'Requisition Raised'),
        ('Sent to CHQ', 'Sent to CHQ'),
        ('In Stock', 'In Stock'),
        ('Delivered', 'Delivered'),
        ('Stock OUT', 'Stock OUT')
    )
    product_condition = models.CharField(max_length=50, choices=PRODUCT_CONDITION,
                                        default='Requisition Raised', verbose_name='Product Condition')
    chalan = models.CharField(max_length=100, null=True, blank=True, verbose_name='Chalan No')
    reference = models.CharField(max_length=100, null=True, blank=True, verbose_name='Reference')
    creator = models.ForeignKey(User, related_name='inventory_creator', on_delete=models.SET_NULL, null=True)
    used_by = models.ForeignKey(User, related_name='inventory_user', on_delete=models.SET_NULL, null=True, blank=True)
    attachment = models.FileField(upload_to='inventory', verbose_name='Chalan Hard Copy')
    date_created = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.used_by}---id : {self.id}--{self.product}'
    

class PhoneModel(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

class Phone(models.Model):
    mac_address = models.CharField(max_length=100, unique=True, verbose_name='MAC Address')
    ext = models.CharField(max_length=4, null=True, blank=True, verbose_name='EXT')
    model = models.ForeignKey(PhoneModel, on_delete=models.SET_NULL, null=True, blank=True)
    ADAPTER_CONDITION = (
        ('Yes', "Yes"),
        ('No', 'No')
    )
    power_adapter = models.CharField(max_length=50, choices=ADAPTER_CONDITION, null=True, 
                                        blank=True, verbose_name='Power Adapter')
    display_name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Display Name')
    provided_ip = models.GenericIPAddressField(unique=True, null=True, blank=True, verbose_name='Phone IP')
    PHONE_CONDITION = (
        ('Reserved', "Reserved"),
        ('In Used', 'In Used'),
        ('Repair', 'Repair'),
        ('Decommission', 'Decommission'),
        ('Not Used', 'Not Used'),
    )
    phone_condition = models.CharField(max_length=50, choices=PHONE_CONDITION,
                                        default='Reserved', verbose_name='Phone Condition')

    SHARE_MODE = (
        ('Single', "Single"),
        ('Multiple', 'Multiple'),
    )
    share_mode = models.CharField(max_length=50, choices=SHARE_MODE,
                                verbose_name='Sharing Mode', null=True, blank=True)

    remarks = models.CharField(max_length=250, null=True, blank=True)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    emp_id = models.CharField(max_length=30, null=True, blank=True, verbose_name='Employee ID')
    name = models.CharField(max_length=100, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)

    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, blank=True)

    switch_port = models.CharField(max_length=30, blank=True, null=True, verbose_name='Switch Port')

    creator = models.ForeignKey(User, related_name='phone_creator', on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)


    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "CISCO Phone Inventory List"

    def __str__(self):
        return self.mac_address

    def get_absolute_url(self):
        return reverse('phone-detail', kwargs={'pk': self.pk})


class Test(models.Model):
    chalan = models.CharField(max_length=50)

    copy = models.FileField(upload_to='test', null=True, blank=True, verbose_name='Chalan Hard Copy')


    class Meta:
        verbose_name_plural = "Test Upload"

    def __str__(self):
        return self.chalan