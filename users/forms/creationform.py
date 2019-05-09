from django import forms
from django.contrib.auth.models import User
from users.models import Profile


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    username = forms.CharField(label='username',
                    widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.CharField(label='email',
                    widget=forms.TextInput(attrs={'placeholder': 'email'}))


    class Meta:
        model = User
        fields = ("username", "email", )


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class ProfileCreationForm(forms.ModelForm):
    zip = forms.IntegerField(label='zip',
                    widget=forms.NumberInput(attrs={'placeholder': 'zip'}))
    profile_image = forms.CharField(label='profile_image', widget=forms.TextInput)
    street = forms.CharField(label='street',
                    widget=forms.TextInput(attrs={'placeholder': 'street name'}))
    housenumber = forms.IntegerField(label='housenumber',
                    widget=forms.NumberInput(attrs={'placeholder': 'House number'}))
    ssn = forms.CharField(label='ssn',
                    widget=forms.TextInput(attrs={'placeholder': 'SSN'}))


    class Meta:
        model = Profile
        fields = ('zip', 'profile_image', 'street', 'housenumber', 'ssn')

    def save(self, user_id, commit=True):
        profile = super(ProfileCreationForm, self).save(commit=False)
        profile.set_user(user_id)
        profile.save()
        return profile