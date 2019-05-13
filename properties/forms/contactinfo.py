from django import forms
from properties.models import ContactInfo



class ContactInfoCreationForm(forms.ModelForm):
    postcode = forms.IntegerField(label='postcode', widget=forms.TextInput(attrs={'placeholder': 'zip code'}))
    street = forms.CharField(label='street_name', widget=forms.TextInput(attrs={'placeholder': 'street name'}))
    house_number = forms.IntegerField(label='house_number', widget=forms.NumberInput(attrs={'placeholder': 'house number'}))
    city = forms.CharField(label='city', widget=forms.TextInput(attrs={'placeholder': 'city'}))
    ssn = forms.IntegerField(label='ssn', widget=forms.NumberInput(attrs={'placeholder': 'social security number'}))
    country = forms.ChoiceField(label='country', widget=forms.Select(attrs={'placeholder': 'country'}))


    class Meta:
        model = ContactInfo
        fields = ('postcode', 'street_name', 'house_number', 'city', 'ssn', 'country')


    def save(self, seller, verified, postcode, commission, commit=True):
        profile = super(CastleCreationForm, self).save(commit=False)
        profile.seller = seller
        profile.postcode = Postcode.objects.filter(postcode=postcode).first()
        profile.verified = verified
        profile.commission = commission
        profile.save()
        return profile