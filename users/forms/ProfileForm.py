from django import forms
from django.forms import ModelForm
from django.forms import widgets
from django.contrib.auth.models import User
from users.models import Profile, Postcode

class ProfileForm(ModelForm):
    first_name = forms.CharField(label='first_name',
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'first name', 'class': 'form-input-field', 'value': 'profile.user.first_name'}))
    last_name = forms.CharField(label='last_name',
                                widget=forms.TextInput(attrs={'placeholder': 'last name', 'class': 'form-input-field'}))

    class Meta:
            model = Profile
            exclude = ['user', 'id']
            widgets = {
            'profile_image': widgets.TextInput(attrs={'class': 'form-control'}),
                'first_name': widgets.TextInput(attrs={'class': 'form-control'}),
                'last_name':widgets.TextInput(attrs={'class': 'form-control'}),
        }
