from django import forms
from properties.models import CastleOffer


class OfferCreationForm(forms.ModelForm):
    offer = forms.CharField(label='price', widget=forms.TextInput(attrs={'placeholder': 'price'}))
    info = forms.CharField(label='info', widget=forms.TextInput(attrs={'placeholder': 'Describe it in vivid detail'}))


    class Meta:
        model = CastleOffer
        fields = ('offer', 'info')


    def save(self, buyer, castle, commit=True):
        profile = super(OfferCreationForm, self).save(commit=False)
        profile.buyer = buyer
        profile.castle = castle
        profile.save()
        return profile
