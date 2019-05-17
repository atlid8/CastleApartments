from django import forms
from django.forms import ModelForm
from django.forms import widgets
from django.contrib.auth.models import User
from users.models import Profile, Postcode

class ProfileForm(ModelForm):
    """Form sem tekur inn upplýsingar um notanda og býr til prófæl tengdan við notanda"""
    class Meta:
            model = Profile
            exclude = ['user', 'id']
            widgets = {
            'profile_image': widgets.TextInput(attrs={'class': 'form-control'}),
        }


class UserEditForm(ModelForm):
    """Form sem að gerir notanda kleift að breyta ulýsingum um sig"""
    class Meta:
            model = User
            exclude = ['id', 'password', 'last_login', 'is_superuser', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions']
            widgets = {
                'first_name': widgets.TextInput(attrs={'class': 'form-control'}),
                'last_name':widgets.TextInput(attrs={'class': 'form-control'}),
        }