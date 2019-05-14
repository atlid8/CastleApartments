from django import forms
from properties.models import ContactInfo
from users.models import Countries


class ContactInfoCreationForm(forms.ModelForm):
    all_countries = [("", "country")]
    countries_objects = Countries.objects.all()
    for countries in countries_objects:
        all_countries.append((countries.country, countries.country))


    postal_code = forms.IntegerField(label='postcode', widget=forms.NumberInput(attrs={'placeholder': ' zip code'}))
    street_name = forms.CharField(label='street_name', widget=forms.TextInput(attrs={'placeholder': ' street name'}))
    house_number = forms.IntegerField(label='house_number', widget=forms.NumberInput(attrs={'placeholder': ' house number'}))
    city = forms.CharField(label='city', widget=forms.TextInput(attrs={'placeholder': ' city'}))
    ssn = forms.IntegerField(label='ssn', widget=forms.NumberInput(attrs={'placeholder': ' social security number'}))
    country = forms.ChoiceField(label='country', choices=all_countries)


    class Meta:
        model = ContactInfo
        fields = ('postal_code', 'street_name', 'house_number', 'city', 'ssn', 'country')


    def save(self, user, commit=True):
        profile = super(ContactInfoCreationForm, self).save(commit=False)
        profile.user = user
        profile.save()
        return profile