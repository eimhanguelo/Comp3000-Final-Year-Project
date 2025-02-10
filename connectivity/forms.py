# Standard library imports
from cProfile import label
from unicodedata import name
from urllib import request

# Django imports
from django import forms
from django.contrib.auth.models import User

# Application-specific imports
from hardware.models import Inventory
from .models import *

class LanForm(forms.ModelForm):
    class Meta:
        model = Lan
        fields = ['ip_address', 'computer_name', 'ip_used', 'os', 'vlan', 'cpu_model', 'cable_tag', 
                  'switch_name', 'switch_port', 'printer_model', 'scanner_model', 'remarks',
                  'used_by', 'location', 'floor', 'instrument_name', 'instrument_id']
        labels = {field: '' for field in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add 'form-control' class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Custom placeholders
        self.fields['ip_address'].widget = forms.TextInput(attrs={'placeholder': 'Enter IP Address'})
        self.fields['computer_name'].widget = forms.TextInput(attrs={'placeholder': 'Enter Computer Name'})
        self.fields['vlan'].widget = forms.TextInput(attrs={'placeholder': 'Enter VLAN'})
        self.fields['cable_tag'].widget = forms.TextInput(attrs={'placeholder': 'Enter Cable Tag'})
        self.fields['switch_port'].widget = forms.TextInput(attrs={'placeholder': 'Enter Switch Port'})
        self.fields['instrument_id'].widget = forms.TextInput(attrs={'placeholder': 'Enter Instrument ID'})
        self.fields['instrument_name'].widget = forms.TextInput(attrs={'placeholder': 'Enter Instrument Name'})

        # Special handling for 'remarks' field with a larger text area
        self.fields['remarks'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter Notes or Remarks'})

        # Handle 'used_by' field queryset depending on the form data or instance
        self.fields['used_by'].queryset = User.objects.none()

        if 'used_by' in self.data:
            self.fields['used_by'].queryset = User.objects.all()
        elif self.instance.pk:
            if self.instance.used_by is None:
                self.fields['used_by'].queryset = User.objects.all()
            else:
                self.fields['used_by'].queryset = User.objects.filter(pk=self.instance.used_by.pk)
        else:
            self.fields['used_by'].queryset = User.objects.none()

    def clean_used_by(self):
        used_by = self.cleaned_data.get('used_by')
        return used_by


class LanRequestForm(forms.ModelForm):

    class Meta:
        model = LanRequest
        fields = ['justification', 'recommended_hod']
        labels = {
            'justification': '',
            'recommended_hod': ''
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set widget for 'justification' field
        self.fields['justification'].widget = forms.Textarea(attrs={
            'placeholder': "Please provide the justification for requesting computer LAN connectivity",
            'rows': 3,
            'class': 'form-control'
        })

        # Apply 'form-control' class and custom attributes to all fields
        self._apply_field_widgets()

        # Apply custom attributes to specific fields
        self._apply_specific_field_widgets()

        # Set up the recommendation fields dynamically
        self._set_recommendation_fields()

    def _apply_field_widgets(self):
        """Apply common widget attributes (e.g., form-control class) to all fields."""
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')

    def _apply_specific_field_widgets(self):
        """Apply specific attributes to particular fields."""
        self.fields['recommended_hod'].widget.attrs.update({
            'id': 'id_recommended_by_all',
        })

    def _set_recommendation_fields(self):
        """Set up the querysets for recommendation fields and customize labels."""
        recommendation_fields = {
            'recommended_hod': User.objects.all(),
        }

        for field_name, queryset in recommendation_fields.items():
            self.fields[field_name].queryset = queryset
            self.fields[field_name].label_from_instance = self._get_user_label
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control select2',
                'data-placeholder': f'Select {field_name.replace("_", " ").title()}'
            })

            # Conditionally set the queryset if the instance already exists
            if self.instance.pk:
                self._set_related_instance(field_name, queryset)

    def _get_user_label(self, user):
        """Return a customized label for user instances."""
        return f"{user.first_name}" 

    def _set_related_instance(self, field_name, queryset):
        """Restrict the queryset to include only the related instance if it exists."""
        related_instance = getattr(self.instance, field_name, None)
        if related_instance:
            self.fields[field_name].queryset = queryset.filter(pk=related_instance.pk)

class LanRequestSignForm(forms.ModelForm):
    class Meta:
        model = LanRequestSign
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class LanRequestITForm(forms.ModelForm):
    class Meta:
        model = LanRequestIT
        fields = [ 'required_ip_address'] 
        labels = {field: '' for field in fields}

class LanRequestITForm(forms.ModelForm):

    class Meta:
        model = LanRequestIT
        fields = ['required_ip_address']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['required_ip_address'].queryset = Lan.objects.none()
        
            if 'required_ip_address' in self.data:
                self.fields['required_ip_address'].queryset = Lan.objects.filter(ip_used=False)
        
            elif self.instance.pk:
                self.fields['required_ip_address'].queryset = Lan.objects.all().filter(pk=self.instance.required_ip_address.pk, ip_used=False)


class LanTransferForm(forms.ModelForm):
    transfer_list = forms.ModelMultipleChoiceField(
        queryset=Product.objects.none(),  # Default to an empty queryset
        widget=forms.CheckboxSelectMultiple,  # Display as checkboxes
        required=False
    )
    purpose_of_transfer = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),  # Multi-line text area
        required=True
    )

    class Meta:
        model = LanTransfer
        fields = ['current_ip_address', 'transferee_location_old_ip_address', 'new_location', 'new_floor', 'new_department', 'transfer_list', 'purpose_of_transfer', 'recommended_hod', 'recommended_hr']
        help_texts = {
            'transfer_list': 'Select items to include in the transfer list.',
        }
        labels = {field: '' for field in fields} 

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs if needed
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['purpose_of_transfer'].widget = forms.Textarea(attrs={
            'placeholder': "Please enter Justification for LAN Connectivity Transfer",
            'rows': 2
        })
        self.fields['purpose_of_transfer'].label = ''


        # Filter `transfer_list` to show only Products with `transfer_list_item=True`
        self.fields['transfer_list'].queryset = Product.objects.filter(transfer_list_item=True).order_by('name')

        # Filter `current_ip_address` based on the provided data or existing instance
        if 'current_ip_address' in self.data:
            self.fields['current_ip_address'].queryset = Lan.objects.filter(ip_used=True)
        elif self.instance.pk:
            self.fields['current_ip_address'].queryset = Lan.objects.filter(pk=self.instance.current_ip_address.pk, ip_used=True)
        else:
            self.fields['current_ip_address'].queryset = Lan.objects.filter(ip_used=True)

        # Filter `recommended_hod` based on provided data or existing instance
        if 'recommended_hod' in self.data:
            self.fields['recommended_hod'].queryset = User.objects.all()
        elif self.instance.pk and self.instance.recommended_hod:
            self.fields['recommended_hod'].queryset = User.objects.filter(pk=self.instance.recommended_hod.pk)
        else:
            self.fields['recommended_hod'].queryset = User.objects.all()

        # Filter `recommended_hr` based on provided data or existing instance

        self.fields['recommended_hr'].queryset = User.objects.none()

        if 'recommended_hr' in self.data:
            self.fields['recommended_hr'].queryset = User.objects.filter(profile__is_hr=True)
        elif self.instance.pk:
            self.fields['recommended_hr'].queryset = self.instance.recommended_hr.all()

        # Apply custom attributes to specific fields
        self._apply_specific_field_widgets()

        # Set up the recommendation fields dynamically
        self._set_recommendation_fields()


    def _apply_specific_field_widgets(self):
        """Apply specific attributes to particular fields."""
        self.fields['recommended_hod'].widget.attrs.update({
            'id': 'id_recommended_by_all',
        })

    def _set_recommendation_fields(self):
        """Set up the querysets for recommendation fields and customize labels."""
        recommendation_fields = {
            'recommended_hod': User.objects.all(),
        }

        for field_name, queryset in recommendation_fields.items():
            self.fields[field_name].queryset = queryset
            self.fields[field_name].label_from_instance = self._get_user_label
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control select2',
                'data-placeholder': f'Select {field_name.replace("_", " ").title()}'
            })

            # Conditionally set the queryset if the instance already exists
            if self.instance.pk:
                self._set_related_instance(field_name, queryset)

    def _get_user_label(self, user):
        """Return a customized label for user instances."""
        return f"{user.first_name}"

    def _set_related_instance(self, field_name, queryset):
        """Restrict the queryset to include only the related instance if it exists."""
        related_instance = getattr(self.instance, field_name, None)
        if related_instance:
            self.fields[field_name].queryset = queryset.filter(pk=related_instance.pk)

class LanTransferHODForm(forms.ModelForm):
    class Meta:
        model = LanTransferHOD
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class LanTransferHRForm(forms.ModelForm):
    class Meta:
        model = LanTransferHR
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class LanTransferITForm(forms.ModelForm):
    class Meta:
        model = LanTransferIT
        fields = [ 'comment'] 
        labels = {field: '' for field in fields}

class LanInstrumentForm(forms.ModelForm):
    class Meta:
        model = LanInstrument
        fields = ['instrument_name', 'instrument_id', 'justification', 'recommended_hod']
        labels = {field: '' for field in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recommended_hod'].queryset = User.objects.none()

        # Add placeholders for 'instrument_name', 'instrument_id', and 'justification'
        self.fields['instrument_name'].widget.attrs.update({
            'placeholder': 'Enter Instrument Name'
        })
        self.fields['instrument_id'].widget.attrs.update({
            'placeholder': 'Enter Instrument ID'
        })
        self.fields['justification'].widget = forms.Textarea(attrs={
            'placeholder': "Please enter Justification for Instrument LAN Connectivity",
            'rows': 3
        })

        # Set the queryset for 'recommended_hod' field
        if 'recommended_hod' in self.data:
            self.fields['recommended_hod'].queryset = User.objects.all()
        elif self.instance.pk:
            self.fields['recommended_hod'].queryset = User.objects.filter(pk=self.instance.recommended_hod.pk)

        # Apply custom attributes to specific fields
        self._apply_specific_field_widgets()

        # Set up the recommendation fields dynamically
        self._set_recommendation_fields()


    def _apply_specific_field_widgets(self):
        """Apply specific attributes to particular fields."""
        self.fields['recommended_hod'].widget.attrs.update({
            'id': 'id_recommended_by_all',
        })

    def _set_recommendation_fields(self):
        """Set up the querysets for recommendation fields and customize labels."""
        recommendation_fields = {
            'recommended_hod': User.objects.all(),
        }

        for field_name, queryset in recommendation_fields.items():
            self.fields[field_name].queryset = queryset
            self.fields[field_name].label_from_instance = self._get_user_label
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control select2',
                'data-placeholder': f'Select {field_name.replace("_", " ").title()}'
            })

            # Conditionally set the queryset if the instance already exists
            if self.instance.pk:
                self._set_related_instance(field_name, queryset)

    def _get_user_label(self, user):
        """Return a customized label for user instances."""
        return f"{user.first_name}"

    def _set_related_instance(self, field_name, queryset):
        """Restrict the queryset to include only the related instance if it exists."""
        related_instance = getattr(self.instance, field_name, None)
        if related_instance:
            self.fields[field_name].queryset = queryset.filter(pk=related_instance.pk)



class LanInstrumentSignForm(forms.ModelForm):
    class Meta:
        model = LanInstrumentSign
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class LanInstrumentITForm(forms.ModelForm):
    class Meta:
        model = LanInstrumentIT
        fields = ['required_ip_address']
        labels = {field: '' for field in fields}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['required_ip_address'].queryset = Lan.objects.none()
        
            if 'required_ip_address' in self.data:
                self.fields['required_ip_address'].queryset = Lan.objects.all()
        
            elif self.instance.pk:
                self.fields['required_ip_address'].queryset = Lan.objects.all().filter(pk=self.instance.required_ip_address.pk)



class LanTransferInstrumentForm(forms.ModelForm):
    transfer_list = forms.ModelMultipleChoiceField(
        queryset=Product.objects.none(),  # Default to an empty queryset
        widget=forms.CheckboxSelectMultiple,  # Display as checkboxes
        required=False
    )
    purpose_of_transfer = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),  # Multi-line text area
        required=True
    )

    class Meta:
        model = LanTransferInstrument
        fields = [
            'current_ip_address', 'current_location', 'current_floor', 'current_department',
            'new_location', 'new_floor', 'new_department', 'contact_person',
            'purpose_of_transfer', 'recommended_hod', 'recommended_hr'
        ]
        help_texts = {
            'transfer_list': 'Select items to include in the transfer list.',
        }
        labels = {field: '' for field in fields}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Capture user from kwargs if passed
        super().__init__(*args, **kwargs)

        # Initialize and customize fields
        self.fields['purpose_of_transfer'].widget = forms.Textarea(attrs={
            'placeholder': "Please enter Justification for Instrument LAN Connectivity Transfer",
            'rows': 3
        })
        self.fields['purpose_of_transfer'].label = ''

        # Filter `current_ip_address` based on provided data or existing instance
        self._set_instance_based_queryset(
            field_name='current_ip_address',
            queryset=Lan.objects.filter(ip_used=True)
        )

        # Filter `recommended_hod` field based on the instance or all users
        self._set_instance_based_queryset(
            field_name='recommended_hod',
            queryset=User.objects.all()
        )

        # Filter `recommended_hr` field based on `profile__is_hr`
        if hasattr(User, 'profile') and hasattr(User.profile, 'is_hr'):
            self.fields['recommended_hr'].queryset = User.objects.filter(profile__is_hr=True)
        elif self.instance.pk:
            self.fields['recommended_hr'].queryset = self.instance.recommended_hr.all()
        else:
            self.fields['recommended_hr'].queryset = User.objects.none()

        # Apply custom attributes to specific fields
        self._apply_specific_field_widgets()

        # Set up the recommendation fields dynamically
        self._set_recommendation_fields()

    def _apply_specific_field_widgets(self):
        """Apply specific attributes to particular fields."""
        self.fields['recommended_hod'].widget.attrs.update({
            'id': 'id_recommended_by_all',
        })
        self.fields['contact_person'].widget.attrs.update({
            'id': 'id_all_users',
        })

    def _set_recommendation_fields(self):
        """Set up the querysets for recommendation fields and customize labels."""
        recommendation_fields = {
            'recommended_hod': User.objects.all(),
            'contact_person': User.objects.all(),
        }

        for field_name, queryset in recommendation_fields.items():
            self.fields[field_name].queryset = queryset
            self.fields[field_name].label_from_instance = self._get_user_label
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control select2',
                'data-placeholder': f'Select {field_name.replace("_", " ").title()}'
            })

            # Conditionally set the queryset if the instance already exists
            self._set_instance_based_queryset(field_name, queryset)

    def _get_user_label(self, user):
        """Return a customized label for user instances."""
        return f"{user.first_name}"

    def _set_instance_based_queryset(self, field_name, queryset):
        """Restrict the queryset for a field to include only the related instance if it exists."""
        if self.instance.pk:
            related_instance = getattr(self.instance, field_name, None)
            if related_instance:
                self.fields[field_name].queryset = queryset.filter(pk=related_instance.pk)
        else:
            self.fields[field_name].queryset = queryset

    def clean_purpose_of_transfer(self):
        """Custom validation for purpose_of_transfer."""
        data = self.cleaned_data['purpose_of_transfer']
        if len(data) < 10:
            raise forms.ValidationError("The purpose must be at least 10 characters long.")
        return data

    def clean(self):
        """Cross-field validation to ensure logical consistency."""
        cleaned_data = super().clean()
        current_department = cleaned_data.get('current_department')
        new_department = cleaned_data.get('new_department')

        if current_department and new_department and current_department == new_department:
            raise forms.ValidationError("Current and new departments cannot be the same.")

        return cleaned_data

class LanTransferInstrumentHODForm(forms.ModelForm):
    class Meta:
        model = LanTransferInstrumentHOD
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class LanTransferInstrumentHRForm(forms.ModelForm):
    class Meta:
        model = LanTransferInstrumentHR
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}


class LanTransferInstrumentITForm(forms.ModelForm):
    class Meta:
        model = LanTransferInstrumentIT
        fields = ['required_ip_address', 'comment']
        labels = {field: '' for field in fields}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['required_ip_address'].queryset = Lan.objects.none()
        
            if 'required_ip_address' in self.data:
                self.fields['required_ip_address'].queryset = Lan.objects.all()
        
            elif self.instance.pk:
                self.fields['required_ip_address'].queryset = Lan.objects.all().filter(pk=self.instance.required_ip_address.pk)


class InternetCreationForm(forms.ModelForm):
    class Meta:
        model = Internet
        fields = ['justification', 'recommended_hod', 'recommended_hr']

        labels={
            'recommended_hod': 'Recommended HOD',
            'recommended_hr': 'Recommended HR',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recommended_hod'].queryset = User.objects.none()

        if 'recommended_hod' in self.data:
            self.fields['recommended_hod'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['recommended_hod'].queryset = User.objects.all().filter(pk=self.instance.recommended_hod.pk)

         # ----------------------------------------------------------------

        self.fields['recommended_hr'].queryset = User.objects.none()

        if 'recommended_hr' in self.data:
            self.fields['recommended_hr'].queryset = User.objects.all().filter(profile__is_hr=True)

        elif self.instance.pk:
            self.fields['recommended_hr'].queryset = User.objects.all().filter(pk=self.instance.recommended_hr.pk, profile__is_hr=True)

class PermissionCreationForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['computer_name', 'ip_address', 'permission_type', 
        'justification', 'recommended_hod','recommended_hr']

        labels={
            'computer_name': 'Computer Name',
            'ip_address' : 'IP Address',
            'permission_type': 'Permission Type',
            'recommended_hod': 'Recommended HOD',
            'recommended_hr': 'Recommended HR',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recommended_hod'].queryset = User.objects.none()

        if 'recommended_hod' in self.data:
            self.fields['recommended_hod'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['recommended_hod'].queryset = User.objects.all().filter(pk=self.instance.recommended_hod.pk)

        self.fields['recommended_hr'].queryset = User.objects.none()

        if 'recommended_hr' in self.data:
            self.fields['recommended_hr'].queryset = User.objects.all().filter(profile__is_hr=True)

        elif self.instance.pk:
            self.fields['recommended_hr'].queryset = User.objects.all().filter(pk=self.instance.recommended_hr.pk, profile__is_hr=True)


class FileAccessForm(forms.ModelForm):
    class Meta:
        model = FileAccess
        fields = [ 'other_dept_head', 'recommended_by','recommended_hod',  'revoke_access']

        labels = {field: '' for field in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['revoke_access'].widget = forms.Textarea(attrs={
            'placeholder': "Please enter the link to be revoked",
            'rows': 2
        })
        #--------------------------recommended by section-----------------------------------------------------
        self.fields['recommended_by'].queryset = User.objects.none()
        self.fields['revoke_access'].widget.attrs['placeholder'] = "Please enter the link to be revoked"

        if 'recommended_by' in self.data:
            self.fields['recommended_by'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['recommended_by'].queryset = User.objects.all().filter(pk=self.instance.recommended_by.pk)

        #--------------------------recommended HOD section-----------------------------------------------------

        self.fields['recommended_hod'].queryset = User.objects.none()

        if 'recommended_hod' in self.data:
            self.fields['recommended_hod'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['recommended_hod'].queryset = User.objects.all().filter(pk=self.instance.recommended_hod.pk)

        #--------------------------other department HOD section-----------------------------------------------------
        self.fields['other_dept_head'].queryset = User.objects.none()

        if 'other_dept_head' in self.data:
            self.fields['other_dept_head'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['other_dept_head'].queryset = User.objects.all().filter(pk=self.instance.other_dept_head.pk)


class FileAccessOtherHODForm(forms.ModelForm):
    class Meta:
        model = FileAccessOtherHOD
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class FileAccessSignForm(forms.ModelForm):
    class Meta:
        model = FileAccessSign
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class FileAccessHODForm(forms.ModelForm):
    class Meta:
        model = FileAccessHOD
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class FileAccessITForm(forms.ModelForm):
    class Meta:
        model = FileAccessIT
        fields = ['comment'] 
        labels = {field: '' for field in fields}

class FileLinkForm(forms.ModelForm):
    class Meta:
        model = FileLink
        fields = ['link_name', 'permission_type', 'location']

        labels = {
            'link_name': 'File Server Address: \\\\fileserver.com\\myfiles',
            'location': 'File Location',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['link_name'].widget.attrs['placeholder'] = "Please specify the folder name here. Ex: QA\EQMS"
        