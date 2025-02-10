from django import forms
from .models import *
from django.contrib.auth.models import User




class DateTimePickerInput(forms.DateTimeInput):
        input_type = 'datetime'

class OpportunityTagCreationForm(forms.ModelForm):
    
    class Meta:
        model = OpportunityTag
        fields = ['idea_giver', 'supervisor', 'title', 'description',
                  'benefits', 'attachment']
        labels = {
            'idea_giver' : 'Idea Giver',
            'supervisor': 'Supervisor (of the Idea Giver)',
            'description': 'Description (What?)',
            'benefits': 'Benefits (Why?)'   
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #----------------------------------------------------------------

        self.fields['idea_giver'].queryset = User.objects.none()

        if 'idea_giver' in self.data:
            self.fields['idea_giver'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['idea_giver'].queryset = User.objects.all().filter(pk=self.instance.idea_giver.pk)

    #     #----------------------------------Supervisor----------------------------------------

        self.fields['supervisor'].queryset = User.objects.none()

        if 'supervisor' in self.data:
            self.fields['supervisor'].queryset = User.objects.all()

        elif self.instance.pk:
            self.fields['supervisor'].queryset = User.objects.all().filter(pk=self.instance.supervisor.pk)



class ObservationTagCreationForm(forms.ModelForm):
    observation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ObservationTag
        fields = ['title', 'observation_date', 'description', 'attachment']
    
        labels = {
            'observation_date': 'Date of Observation',
            'description': 'Description (What?)', 
        }






