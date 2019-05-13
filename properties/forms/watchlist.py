from django import forms
from properties.models import Watchlist



class WatchlistCreationForm(forms.ModelForm):

    class Meta:
        model = Watchlist
        fields = ()

    def save(self, castle, user, commit=True):
        profile = super(WatchlistCreationForm, self).save(commit=False)
        profile.castle_watch = castle
        profile.user =user
        profile.save()
        return profile