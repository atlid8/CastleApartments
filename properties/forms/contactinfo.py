from django import forms
from properties.models import ContactInfo



class ContactInfoCreationFrom(forms.ModelForm):
    name = forms.CharField(label='name',
                    widget=forms.TextInput(attrs={'placeholder': 'castle name'}))
    postcode = forms.CharField(label='postcode', widget=forms.TextInput(attrs={'placeholder': 'zip code', 'disabled':'disabled'}))
    street = forms.CharField(label='street name',
                    widget=forms.TextInput(attrs={'placeholder': 'street name'}))
    house_number = forms.IntegerField(label='house_number',
                    widget=forms.NumberInput(attrs={'placeholder': 'house number'}))
    rooms = forms.CharField(label='rooms', widget=forms.TextInput(attrs={'placeholder': 'rooms'}))
    price = forms.CharField(label='price', widget=forms.TextInput(attrs={'placeholder': 'price'}))
    size = forms.CharField(label='size', widget=forms.TextInput(attrs={'placeholder': 'size (m2)'}))
    info = forms.CharField(label='info', widget=forms.TextInput(attrs={'placeholder': 'describe it in vivid detail'}))


    class Meta:
        model = Castle
        fields = ('name', 'house_number', 'street', 'rooms', 'price', 'size', 'info')


    def save(self, seller, verified, postcode, commission, commit=True):
        profile = super(CastleCreationForm, self).save(commit=False)
        profile.seller = seller
        profile.postcode = Postcode.objects.filter(postcode=postcode).first()
        profile.verified = verified
        profile.commission = commission
        profile.save()
        return profile