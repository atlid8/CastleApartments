from django import forms
from properties.models import ContactInfo
from users.models import Countries

all_countries = [("", "country")]
countries_objects = Countries.objects.all()  # Til að geta látið fólk velja úr öllum löndum heimsins
for countries in countries_objects:
    all_countries.append((countries.country, countries.country))


class ContactInfoCreationForm(forms.ModelForm):
    """Form sem tekur inn og vistar contact info um kaupanda"""

    postal_code = forms.IntegerField(min_value=1, max_value=1000, label='postcode', widget=forms.NumberInput(attrs={'placeholder': ' zip code'}))
    street_name = forms.CharField(label='street_name', widget=forms.TextInput(attrs={'placeholder': ' street name'}))
    house_number = forms.IntegerField(min_value=1, label='house_number', widget=forms.NumberInput(attrs={'placeholder': ' house number'}))
    city = forms.CharField(label='city', widget=forms.TextInput(attrs={'placeholder': ' city'}))
    ssn = forms.IntegerField(min_value = 1000000000, max_value=9999999999,label='ssn', widget=forms.NumberInput(attrs={'placeholder': ' social security number'}))
    country = forms.ChoiceField(label='country', choices=all_countries)


    class Meta:
        model = ContactInfo
        fields = ('postal_code', 'street_name', 'house_number', 'city', 'ssn', 'country')


    def save(self, user, commit=True):
        """FAll sem vistar upplýsingar um kaupanda"""
        profile = super(ContactInfoCreationForm, self).save(commit=False)
        profile.user = user
        profile.save()
        return profile