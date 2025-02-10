from cProfile import label
from math import floor
from django import forms
from .models import *
from django.contrib.auth.models import User


from django import forms
from .models import Eticket

from django import forms
from .models import Eticket

from django import forms
from .models import Eticket
from ckeditor.widgets import CKEditorWidget  # Import the CKEditorWidget

class TicketCreationForm(forms.ModelForm):
    class Meta:
        model = Eticket
        fields = ['problem_category', 'ip_address', 'problem_description', 'reference_form', 'eticket_attachment']

        labels = {
            'problem_category': '',
            'ip_address': '',
            'reference_form': '',
            'eticket_attachment': '',
            'problem_description': '',
        }

        # Here we apply CKEditor to the problem_description field
        widgets = {
            'problem_description': CKEditorWidget(attrs={'placeholder': 'Describe the issue in detail...', 'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'placeholder': 'Enter IP address (e.g., 172.25.1.102)', 'class': 'form-control'}),
            'reference_form': forms.TextInput(attrs={'placeholder': 'Enter reference (e.g., SOP/IT/0098/02, Appendix A)', 'class': 'form-control'}),
            'eticket_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.created_via = 'MANUAL'  # Set the creation source
        if commit:
            instance.save()
            # update_change_reason(instance, 'Created a new Eticket')
        return instance

class AssignForm(forms.ModelForm):
    class Meta:
        model = EAssign
        fields = ['engineer', 'assign_type']
        labels = {field: '' for field in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize engineer queryset based on instance or provided data
        self.fields['engineer'].queryset = User.objects.none()
        if self.instance.pk and self.instance.engineer:
            self.fields['engineer'].queryset = User.objects.filter(pk=self.instance.engineer.pk)
        elif 'engineer' in self.data:
            try:
                engineer_id = self.data.get('engineer')
                self.fields['engineer'].queryset = User.objects.filter(pk=engineer_id)
            except (ValueError, TypeError):
                pass

        # Apply common and specific widget attributes
        self._apply_field_widgets()
        self._apply_specific_field_widgets()

        # Set up dynamic recommendation fields
        self._set_recommendation_fields()

    def _apply_field_widgets(self):
        """Apply common widget attributes (e.g., form-control class) to all fields."""
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def _apply_specific_field_widgets(self):
        """Update widgets for specific fields with additional settings."""
        self.fields['engineer'].widget.attrs.update({'id': 'id_recommended_by_all'})

    def _set_recommendation_fields(self):
        """Set up the querysets and attributes for recommendation fields dynamically."""
        recommendation_fields = {
            'engineer': User.objects.all().filter(is_staff=True),
        }

        for field, queryset in recommendation_fields.items():
            self.fields[field].queryset = queryset
            self.fields[field].label_from_instance = self._get_user_label

            # Update attributes for Select2 and placeholders
            self.fields[field].widget.attrs.update({
                'class': 'form-control select2',
                'data-placeholder': f'Select {field.replace("_", " ").title()}'
            })

            # Restrict queryset to instance-related data if available
            if self.instance.pk:
                related_instance = getattr(self.instance, field, None)
                if related_instance:
                    self.fields[field].queryset = queryset.filter(pk=related_instance.pk)

    @staticmethod
    def _get_user_label(obj):
        """Return the label for a user instance. Can be customized further."""
        return obj.first_name


class ESolveForm(forms.ModelForm):
    class Meta:
        model = ESolve
        fields = [ 'solve_type', 'note'] 
        labels = {field: '' for field in fields}
        widgets = {
                    'note': forms.Textarea(attrs={'rows': 2}),
                }

class EDiscussionForm(forms.ModelForm):
    class Meta:
        model = EDiscussion
        fields = [ 'discussion'] 
        labels = {field: '' for field in fields}
        widgets = {
                    'discussion': forms.Textarea(attrs={'rows': 2}),
                }

class EEInternalForm(forms.ModelForm):
    class Meta:
        model = EInternal
        fields = [ 'discussion'] 
        labels = {field: '' for field in fields}
        widgets = {
                    'discussion': forms.Textarea(attrs={'rows': 2}),
                }