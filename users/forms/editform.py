from django import forms
from django.contrib.auth.models import User
from users.models import Profile, Postcode


class BuyerEditForm(forms.ModelForm):
    postcode = forms.CharField(label='postcode',
                    widget=forms.TextInput(attrs={'placeholder': 'postcode', 'class':'form-input-field'}))
    profile_image = forms.CharField(label='profile_image', widget=forms.TextInput(attrs={'placeholder': 'profile image', 'class':'form-input-field'}))
    street = forms.CharField(label='street',
                    widget=forms.TextInput(attrs={'placeholder': 'street name', 'class':'form-input-field'}))
    house_number = forms.IntegerField(label='house_number',
                    widget=forms.NumberInput(attrs={'placeholder': 'house number', 'class':'form-input-field'}))
    ssn = forms.CharField(label='ssn',
                    widget=forms.TextInput(attrs={'placeholder': 'ssn', 'class':'form-input-field'}))


    class Meta:
        model = Profile
        fields = ('street', 'house_number', 'ssn')


    def save(self, user_id, postcode, commit=True):
        profile = super(ProfileCreationForm, self).save(commit=False)
        profile.user = user_id
        postcode = Postcode.objects.filter(postcode=postcode).first()
        profile.postcode = postcode
        profile.save()
        return profile
