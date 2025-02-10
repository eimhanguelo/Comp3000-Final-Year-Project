from django import forms
from blog.models import *
from users.models import * 
from connectivity.models import *
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, ButtonHolder, HTML
from multiselectfield.forms.fields import MultiSelectFormField

from django import forms
from .models import *

class EmployeeCreationForm(forms.ModelForm):
    emp_join_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='')

    class Meta:
        model = Employee
        fields = ['fullname', 'emp_id', 'department', 'designation', 'emp_join_date', 
                  'phone', 'location', 'floor', 'ext', 'user_activation', 'mail_activation', 
                  'group_access', 'justification', 'recommended_by', 'approved_hod', 'approved_hr', 'image']
        labels = {field: '' for field in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply 'form-control' class and update widgets for all fields
        self._apply_field_widgets()

        # Update widgets for specific fields with placeholders or custom settings
        self._apply_specific_field_widgets()

        # Set up the recommendation fields dynamically
        self.set_recommendation_fields()

    def _apply_field_widgets(self):
        """Apply common widget attributes (e.g., form-control class) to all fields."""
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def _apply_specific_field_widgets(self):
        """Apply field-specific attributes, placeholders, etc."""
        placeholders = {
            'fullname': 'Enter full name...',
            'emp_id': 'Enter Employee ID...',
            'phone': 'Enter Phone number...',
            'ext': 'Enter Extension number...',
        }

        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({
                'placeholder': placeholder,
            })

        self.fields['justification'].widget = forms.Textarea(attrs={
            'placeholder': "Enter Justification for Mail Creation...",
            'rows': 2,
        })

        # Special handling for recommendation fields
        self.fields['recommended_by'].widget.attrs.update({'id': 'id_recommended_by_all'})
        self.fields['approved_hod'].widget.attrs.update({'id': 'id_approved_hod_all'})

    def set_recommendation_fields(self):
        """Set up the querysets for recommendation fields and optimize with labels."""
        recommendation_fields = {
            'recommended_by': User.objects.all(),
            'approved_hod': User.objects.all(),
        }

        for field, queryset in recommendation_fields.items():
            self.fields[field].queryset = queryset
            self.fields[field].label_from_instance = self._get_user_label

            # Apply Select2 and other attributes
            self.fields[field].widget.attrs.update({
                'class': 'form-control select2',  # Use select2 for better dropdown
                'data-placeholder': f'Select {field.replace("_", " ").title()}'
            })

            # Conditionally set queryset if instance exists
            if self.instance.pk:
                self._set_related_instance(field, queryset)

    def _get_user_label(self, obj):
        """Return the label for a user instance. You can customize this logic further."""
        return obj.first_name

    def _set_related_instance(self, field, queryset):
        """Set the queryset based on related instance if available."""
        related_instance = getattr(self.instance, field)
        if related_instance:
            self.fields[field].queryset = queryset.filter(pk=related_instance.pk)



class EmployeeSignForm(forms.ModelForm):
    class Meta:
        model = EmployeeSign
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class EmployeeHODForm(forms.ModelForm):
    class Meta:
        model = EmployeeHOD
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}


class EmployeeHRForm(forms.ModelForm):
    class Meta:
        model = EmployeeHR
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}


class EmployeeITForm(forms.ModelForm):
    class Meta:
        model = EmployeeIT
        fields = ['mail_id', 'mail_box', 'admin_comment'] 
        labels = {field: '' for field in fields}


class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'justification', 'user_activation', 'mail_activation', 'group_access',
            'recommended_by', 'approved_hod', 'approved_hr'
        ]
        labels = {field: '' for field in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Special handling for fields with custom attributes and styling
        self.setup_field_attributes()

        # Call to set up recommendation fields
        self.set_recommendation_fields()

    def setup_field_attributes(self):
        """Setup attributes for form fields."""
        # Set attributes for recommendation fields
        recommendation_fields = ['recommended_by', 'approved_hod']
        for field in recommendation_fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control select2',  # Use select2 for better dropdown
                'id': f'id_{field}_all',          # Unique ID for each field
                'data-placeholder': f'Select {field.replace("_", " ").title()}'  # Placeholder text
            })

        # Set attributes for 'justification' field
        self.fields['justification'].widget = forms.Textarea(attrs={
            'placeholder': "Enter Justification for Mail Modification...",
            'rows': 2,
            'class': 'form-control'
        })

    def set_recommendation_fields(self):
        """Set up the querysets and labels for recommendation fields."""
        recommendation_fields = {
            'recommended_by': User.objects.all(),
            'approved_hod': User.objects.all(),
        }

        for field, queryset in recommendation_fields.items():
            self.fields[field].queryset = queryset
            self.fields[field].label_from_instance = lambda obj: obj.first_name

            # If the instance has a related user, adjust queryset to the related instance
            if self.instance.pk:
                related_instance = getattr(self.instance, field)
                if related_instance:
                    self.fields[field].queryset = queryset.filter(pk=related_instance.pk)

class AccountSignForm(forms.ModelForm):
    class Meta:
        model = AccountSign
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class AccountHODForm(forms.ModelForm):
    class Meta:
        model = AccountHOD
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}


class AccountHRForm(forms.ModelForm):
    class Meta:
        model = AccountHR
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}


class AccountITForm(forms.ModelForm):
    class Meta:
        model = AccountIT
        fields = [ 'admin_comment'] 
        labels = {field: '' for field in fields}

class ResignationCreationForm(forms.ModelForm):

    DATA_CONDITION = (
        ('transferred', 'Transferred'),
        ('destroyed', 'Destroyed'),
    )
    computer_data = models.CharField(max_length=30, choices=DATA_CONDITION, default='Transferred')
    
    class Meta:
        model = Resignation
        fields = ['computer_data', 'computer_data_receiver', 'email_archive', 'email_archive_receiver',
                  'computer_ip_address', 'common_computer_ip', 'computer_ip_receiver',
                  'ip_phone', 'common_ip_phone', 'ip_phone_receiver', 'printer_owner',
                   'printer_receiever', 'scanner_owner', 'scanner_receiever', 'internet_access',
                   'empower_id', 'internet_access', 'empower_id',
                   'chromeleon_id', 'eqms_id', 'standalone_id', 'recommended_hod']
        labels = {
            'computer_data' : 'Computer Data Condition',
            'computer_data_receiver': 'Receiver of Computer Data',
            'email_archive' : 'Email Archive Status',
            'email_archive_receiver': 'Receiver of Email Archive',
            'computer_ip_address': 'Computer IP Address',
            'common_computer_ip': 'Is your IP address common ?',
            'computer_ip_receiver': 'Receiver of Computer IP',
            'ip_phone': 'IP Phone',
            'common_ip_phone': 'Have you used common IP phone ?',
            'ip_phone_receiver': 'Receiver of IP Phone',
            'printer_owner': 'Are you printer owner ?',
            'printer_receiever': 'Receiver of Printer',
            'scanner_owner': 'Are you scanner owner ?',
            'scanner_receiever': 'Receiver of Scanner',
            'internet_access': 'Have you Internet Access ?',
            'empower_id': "Empower ID",
            'chromeleon_id': 'Chromeleon ID',
            'eqms_id': 'EQMS ID',
            'standalone_id': 'Standalone ID',
            'recommended_hod': 'Recommended HOD Person',     
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['computer_data_receiver'].queryset = User.objects.none()

        if 'computer_data_receiver' in self.data:
            self.fields['computer_data_receiver'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['computer_data_receiver'].queryset = User.objects.all().filter(pk=self.instance.computer_data_receiver.pk)

        
         # ----------------------------------------------------------------

        self.fields['email_archive_receiver'].queryset = User.objects.none()

        if 'email_archive_receiver' in self.data:
            self.fields['email_archive_receiver'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['email_archive_receiver'].queryset = User.objects.all().filter(pk=self.instance.email_archive_receiver.pk)

        # --------------------------------------------------------------------

        self.fields['computer_ip_address'].queryset = Lan.objects.none()

        if 'computer_ip_address' in self.data:
            self.fields['computer_ip_address'].queryset = Lan.objects.all()

        elif self.instance.pk:
            self.fields['computer_ip_address'].queryset = Lan.objects.all().filter(pk=self.instance.computer_ip_address.pk)

        # --------------------------------------------------------------------

        self.fields['computer_ip_receiver'].queryset = User.objects.none()

        if 'computer_ip_receiver' in self.data:
            self.fields['computer_ip_receiver'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['computer_ip_receiver'].queryset = User.objects.all().filter(pk=self.instance.computer_ip_receiver.pk)


        # ----------------------------------------------------------------

        self.fields['ip_phone_receiver'].queryset = User.objects.none()

        if 'ip_phone_receiver' in self.data:
            self.fields['ip_phone_receiver'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['ip_phone_receiver'].queryset = User.objects.all().filter(pk=self.instance.ip_phone_receiver.pk)

        # --------------------------------------------------------------------

        self.fields['printer_receiever'].queryset = User.objects.none()

        if 'printer_receiever' in self.data:
            self.fields['printer_receiever'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['printer_receiever'].queryset = User.objects.all().filter(pk=self.instance.printer_receiever.pk)

        # ----------------------------------------------------------------

        self.fields['scanner_receiever'].queryset = User.objects.none()

        if 'scanner_receiever' in self.data:
            self.fields['scanner_receiever'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['scanner_receiever'].queryset = User.objects.all().filter(pk=self.instance.scanner_receiever.pk)

        # --------------------------------------------------------------------

        self.fields['recommended_hod'].queryset = User.objects.none()

        if 'recommended_hod' in self.data:
            self.fields['recommended_hod'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['recommended_hod'].queryset = User.objects.all().filter(pk=self.instance.recommended_hod.pk)




