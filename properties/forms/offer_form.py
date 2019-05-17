from django import forms
from properties.models import CastleOffer


class OfferCreationForm(forms.ModelForm):
    """Form sem að býr til Tilboð í kastala"""
    offer = forms.CharField(label='price', widget=forms.TextInput(attrs={'placeholder': 'price'}))
    info = forms.CharField(label='info', widget=forms.Textarea(attrs={'placeholder': 'send a message'}))


    class Meta:
        model = CastleOffer
        fields = ('offer', 'info')


    def save(self, buyer, castle, commit=True):
        """Fall sem að vistar tilboð í kastala"""
        profile = super(OfferCreationForm, self).save(commit=False)
        profile.buyer = buyer
        profile.castle = castle
        profile.save()
        return profile
