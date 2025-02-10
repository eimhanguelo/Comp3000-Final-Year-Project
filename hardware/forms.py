from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Requisition, Inventory, Product
from .models import *


class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = [
            'requisition_type', 'cost_center', 'requisition_attachment',
            'recommended_by', 'recommended_hod', 'recommended_hr',
            'recommended_accountant', 'recommended_verifier_it', 'recommended_hod_it'
        ]
        labels = {field: '' for field in fields}
        help_texts = {
            'requisition_type': 'Select requisition type.',
            'cost_center': 'Enter the relevant cost center.',
            'requisition_attachment': 'Attach any relevant documents (if any).',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_recommendation_fields()
        
        self.fields['recommended_by'].widget.attrs.update({'id': 'id_recommended_by_requisitions'})
        self.fields['recommended_hod'].widget.attrs.update({'id': 'id_recommended_hod_requisitions'})
        
        # Apply 'form-control' class to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def set_recommendation_fields(self):
        """Set up the querysets for recommendation fields."""
        # Define fields and their default querysets
        recommendation_fields = {
            'recommended_by': User.objects.all(),
            'recommended_hod': User.objects.all(),
            'recommended_hr': User.objects.filter(profile__is_hr=True),
            'recommended_accountant': User.objects.filter(profile__is_accountant=True),
            'recommended_verifier_it': User.objects.filter(profile__is_verifier_it=True),
            'recommended_hod_it': User.objects.filter(profile__is_hod_it=True)
        }
        # Apply the recommendation fields dynamically
        for field, queryset in recommendation_fields.items():
            self.fields[field].queryset = queryset
            self.fields[field].label_from_instance = lambda obj: obj.first_name
            self.fields[field].widget.attrs.update({
                'data-placeholder': f'Select {field.replace("_", " ").title()}'
            })


class RequisitionSignForm(forms.ModelForm):
    class Meta:
        model = RequisitionSign
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class RequisitionHODForm(forms.ModelForm):
    class Meta:
        model = RequisitionHOD
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class RequisitionHRForm(forms.ModelForm):
    class Meta:
        model = RequisitionHR
        fields = [ 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class RequisitionACCForm(forms.ModelForm):
    class Meta:
        model = RequisitionACC
        fields = ['sign_type', 'new_asset_no', 'comment'] 
        labels = {field: '' for field in fields}

class RequisitionVERIFYForm(forms.ModelForm):
    class Meta:
        model = RequisitionVERIFY
        fields = ['verified_by_it', 'sign_type', 'comment'] 
        labels = {field: '' for field in fields}

class RequisitionHODITForm(forms.ModelForm):
    class Meta:
        model = RequisitionHODIT
        fields = ['sign_type','comment'] 
        labels = {field: '' for field in fields}

class RequisitionITForm(forms.ModelForm):
    class Meta:
        model = RequisitionIT
        fields = ['comment'] 
        labels = {field: '' for field in fields}

class ReqForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'details', 'quantity', 'date_of_last_issue', 'remarks']
        widgets = {
            'date_of_last_issue': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Create a list of product choices with indicators for those requiring an asset number
        self.fields['product'].choices = self._get_product_choices()
        
        # Add a placeholder for the product selection
        self.fields['product'].widget.attrs['placeholder'] = 'Select a product'
        
        # Set clear labels for each field
        self.fields['product'].label = "Product (<span style='color:blue;'>** <span title='Requires Asset Number'>ℹ️</span>)</span>"
        self.fields['details'].label = "Details"
        self.fields['quantity'].label = "Quantity"
        self.fields['date_of_last_issue'].label = "Date of Last Issue"
        self.fields['remarks'].label = "Remarks"

    def _get_product_choices(self):
        """Generate product choices, appending ** for products with an asset number."""
        return [
            (product.id, f"{product.name} **" if product.has_asset_no else product.name)
            for product in Product.objects.all()
        ]

class InventoryForm(forms.ModelForm):
    # attachment = forms.FileField(widget=forms.FileInput, required=False)
    class Meta:
        model = Inventory
        fields = [
            'product', 'model', 'quantity', 'unit_type', 
            'details', 'remarks', 'requisition', 'used_by',
            'product_condition', 'reference', 'chalan', 'attachment'
        ]

        labels = {field: '' for field in fields}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'

        #------------------------------Requisition Dropdown ------------------------------------
            self.fields['requisition'].queryset = Requisition.objects.none()

            if 'requisition' in self.data:
                self.fields['requisition'].queryset = Requisition.objects.all()

            elif self.instance.pk:
                self.fields['requisition'].queryset = Requisition.objects.all().filter(pk=self.instance.requisition.pk)

        
        # ------------------------------------Who Used this Asset----------------------------
            self.fields['used_by'].queryset = User.objects.none()

            if 'used_by' in self.data:
                self.fields['used_by'].queryset = User.objects.all()

            elif self.instance.pk:
                self.fields['used_by'].queryset = User.objects.all().filter(pk=self.instance.used_by.pk)
 


from django_select2 import forms as s2forms

class ModelWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]

class PhoneForm(forms.ModelForm):
   
    class Meta:
        model = Phone
        fields = ['mac_address', 'ext', 'model', 'power_adapter', 'display_name',
                  'provided_ip', 'phone_condition', 'remarks', 'department', 'share_mode',
                  'emp_id', 'name','position', 'switch_port', 'location', 'floor']
     
        labels = {field: '' for field in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            # Set the 'remarks' field as a multi-line Textarea
            if field_name == 'remarks':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 2})  # 3 rows for a larger text area
