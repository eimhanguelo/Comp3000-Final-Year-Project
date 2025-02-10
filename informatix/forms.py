from django import forms
from .models import *
from django.contrib.auth.models import User


class EngineerForm(forms.ModelForm):
    engineer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True))


    class Meta:
        model = ShiftPlan
        fields = ('__all__')
