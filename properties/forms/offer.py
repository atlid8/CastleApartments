from django import forms
from properties.models import CastleOffer


class OfferCreationForm(forms.ModelForm):
    price = forms.CharField(label='price', widget=forms.TextInput(attrs={'placeholder': 'price'}))
    info = forms.CharField(label='info', widget=forms.TextInput(attrs={'placeholder': 'Describe it in vivid detail'}))


    class Meta:
        model = CastleOffer
        fields = ('price', 'info')


    def save(self, buyer, castle, commit=True):
        profile = super(CastleCreationForm, self).save(commit=False)
        profile.seller = seller
        profile.postcode = Postcode.objects.filter(postcode=postcode).first()
        profile.verified = verified
        profile.commission = commission
        profile.save()
        return profile
