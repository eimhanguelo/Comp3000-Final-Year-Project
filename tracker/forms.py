from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from .models import Tracker

class TrackerForm(forms.ModelForm):
    class Meta:
        model = Tracker
        fields = ['category', 'description', 'remarks']
        # Define widgets for each field
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a category'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter a detailed description...'}),
            'remarks': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any additional comments...'}),
        }
        labels = {field: '' for field in fields}

    # Category validation
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise ValidationError("Category cannot be empty!")
        # You can add more specific validation here if necessary
        return category

    # Description validation with length check
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) < 5:
            raise ValidationError("Description should be at least 5 characters long.")
        return description

    # Remarks validation (optional, if needed)
    def clean_remarks(self):
        remarks = self.cleaned_data.get('remarks')
        if remarks and len(remarks) > 500:  # Example limit for remarks
            raise ValidationError("Remarks should not exceed 500 characters.")
        return remarks




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'