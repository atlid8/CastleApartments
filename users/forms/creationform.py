from django import forms
from django.contrib.auth.models import User
from users.models import Profile, Postcode


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class':'form-input-field'}))
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class':'form-input-field'}))
    username = forms.CharField(label='username',
                    widget=forms.TextInput(attrs={'placeholder': 'username', 'class':'form-input-field'}))
    email = forms.CharField(label='email',
                    widget=forms.TextInput(attrs={'placeholder': 'email', 'class':'form-input-field'}))


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
    postcode = forms.CharField(label='postcode',
                    widget=forms.TextInput(attrs={'placeholder': 'postcode', 'class':'form-input-field'}))
    profile_image = forms.CharField(label='profile_image', widget=forms.TextInput(attrs={'placeholder': 'image link', 'class':'form-input-field'}))
    street = forms.CharField(label='street',
                    widget=forms.TextInput(attrs={'placeholder': 'street name', 'class':'form-input-field'}))
    house_number = forms.IntegerField(label='house_number',
                    widget=forms.NumberInput(attrs={'placeholder': 'house number', 'class':'form-input-field'}))
    ssn = forms.CharField(label='ssn',
                    widget=forms.TextInput(attrs={'placeholder': 'ssn', 'class':'form-input-field'}))


    class Meta:
        model = Profile
        fields = ('profile_image', 'street', 'house_number', 'ssn')


    def save(self, user_id, postcode, commit=True):
        profile = super(ProfileCreationForm, self).save(commit=False)
        profile.user = user_id
        postcode = Postcode.objects.filter(postcode=postcode).first()
        profile.postcode = postcode
        profile.save()
        return profile
