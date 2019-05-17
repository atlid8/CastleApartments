from django import forms
from django.contrib.auth.models import User
from users.models import Profile, Postcode


class UserCreationForm(forms.ModelForm):
    """Form sem býr til notanda út frá notendanafni, fyrra og seinna nafni, póstfangi og lykilorði"""
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(min_length=8, label=("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'create password', 'class':'form-input-field'}))
    password2 = forms.CharField(min_length=8, label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'placeholder': 'confirm password', 'class':'form-input-field'}))
    username = forms.CharField(label='username',
                    widget=forms.TextInput(attrs={'placeholder': 'username', 'class':'form-input-field'}))
    email = forms.CharField(label='email',
                    widget=forms.TextInput(attrs={'placeholder': 'e-mail address', 'class':'form-input-field'}))
    first_name = forms.CharField(label='first_name',
                   widget=forms.TextInput(attrs={'placeholder': 'first name','class':'form-input-field'}))
    last_name = forms.CharField(label='last_name',
                                 widget=forms.TextInput(attrs={'placeholder': 'last name', 'class': 'form-input-field'}))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


    def clean_password2(self):
        """Fall sem athugar hvort að lykilorðin séu eins"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


    def save(self, commit=True):
        """FAll sem að vistar notanda án réttinda starfsmanns"""
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def save_staff(self, commit=True):
        """Fall sem að vistar notanda með réttindi starfmanns"""
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        if commit:
            user.save()
        return user