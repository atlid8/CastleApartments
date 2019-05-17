from django import forms
from properties.models import Castle
from properties.models import CastleImage
from users.models import Postcode
from django.forms import ModelForm

postcodes = [("", "postcode")]
postcodes_objects = Postcode.objects.all()
for zip in postcodes_objects:
    postcodes.append((zip.postcode, zip.postcode))

class CastleCreationForm(forms.ModelForm):
    """Form sem tekur inn upplýsingar um kastala og búr hann til"""
    name = forms.CharField(label='name',
                    widget=forms.TextInput(attrs={'placeholder': 'castle name'}))
    postcode = forms.ChoiceField(choices=postcodes)
    street = forms.CharField(label='street name',
                    widget=forms.TextInput(attrs={'placeholder': 'street name'}))
    house_number = forms.IntegerField(label='house_number',
                    widget=forms.NumberInput(attrs={'placeholder': 'house number'}))
    rooms = forms.IntegerField(min_value=1, max_value=50, label='rooms', widget=forms.NumberInput(attrs={'placeholder': 'rooms'}))
    price = forms.IntegerField(min_value=1, max_value=100000, label='price', widget=forms.NumberInput(attrs={'placeholder': 'price'}))
    size = forms.IntegerField(min_value=1, max_value=10000, label='size', widget=forms.NumberInput(attrs={'placeholder': 'size (m2)'}))
    info = forms.CharField(label='info', widget=forms.TextInput(attrs={'placeholder': 'describe it in vivid detail'}))


    class Meta:
        model = Castle
        fields = ('name', 'house_number', 'street', 'rooms', 'price', 'size', 'info')


    def save(self, seller, verified, postcode, commission, commit=True):
        """FAll sem vistar kastala"""
        profile = super(CastleCreationForm, self).save(commit=False)
        profile.seller = seller
        profile.postcode = Postcode.objects.filter(postcode=postcode).first()
        profile.verified = verified#Verified er alltaf False núna en þetta er svona ef við viljum geta látið starfsmenn setja inn verified kastala beint
        profile.commission = commission
        profile.save()
        return profile


class CastleImageCreationForm(forms.ModelForm):
    image = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'link to image'}))


    class Meta:
        model = CastleImage
        fields = ('image',)

    def save(self, castle, commit=True):
        """Fall sem vistar myndir af kastölum inn"""
        profile = super(CastleImageCreationForm, self).save(commit=False)
        profile.castle = castle
        profile.save()
        return profile


class CastleEditForm(ModelForm):
    """Form sem að leyfir manni að breyta uplýsingum um kastala"""
    class Meta:
            model = Castle
            exclude = ['id', 'seller', 'commission', 'verified']
