from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email', 'password1', 'password2')


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name']
        
        labels={
            'first_name': ''
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['first_name'].widget.attrs['readonly'] = True


from django.core.exceptions import ValidationError
from PIL import Image as PILImage
import io

class ProfileUpdateForm(forms.ModelForm):
    emp_join_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=False,
        label=""
    )

    image = forms.ImageField(
        help_text='Upload Image: 1000x1000px, < 1MB', 
        widget=forms.ClearableFileInput(attrs={'class': 'image-upload'}),
        label=""
    )

    class Meta:
        model = Profile
        fields = [
            'emp_id', 'department', 'position', 'emp_join_date', 
            'location', 'floor', 'phone', 'ext', 'image'
        ]
        
        labels = {
            'emp_id': '',
            'department': '',
            'position': '',
            'location': '',
            'floor': '',
            'emp_join_date': '',
            'phone': '',
            'ext': '',
            'image': '',
        }



    

