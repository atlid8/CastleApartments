from django import forms
from properties.models import ContactInfo


marcas = (
        ('westeror', 'Westeros'),
        ('essos', 'Essos'),
        ('always winter', 'The Lands of Always Winter'),)

class ContactInfoCreationForm(forms.ModelForm):
    postal_code = forms.IntegerField(label='postcode', widget=forms.TextInput(attrs={'placeholder': ' zip code'}))
    street_name = forms.CharField(label='street_name', widget=forms.TextInput(attrs={'placeholder': ' street name'}))
    house_number = forms.IntegerField(label='house_number', widget=forms.NumberInput(attrs={'placeholder': ' house number'}))
    city = forms.CharField(label='city', widget=forms.TextInput(attrs={'placeholder': ' city'}))
    ssn = forms.IntegerField(label='ssn', widget=forms.NumberInput(attrs={'placeholder': ' social security number'}))
    country = forms.ChoiceField(choices=marcas)


    class Meta:
        model = ContactInfo
        fields = ('postal_code', 'street_name', 'house_number', 'city', 'ssn', 'country')


    def save(self, user, commit=True):
        profile = super(ContactInfoCreationForm, self).save(commit=False)
        profile.user = user
        profile.save()
        return profile