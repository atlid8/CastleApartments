from django import forms
from properties.models import Watchlist



class WatchlistCreationForm(forms.ModelForm):

    class Meta:
        model = Watchlist
        fields = ()

    def save(self, castle, commit=True):
        profile = super(CastleImageCreationForm, self).save(commit=False)
        profile.castle = castle
        profile.save()
        return profile