from django import forms
from properties.models import Watchlist



class WatchlistCreationForm(forms.ModelForm):
    """Form sem tekur inn að bætir eignum á watchlist notenda"""

    class Meta:
        model = Watchlist
        fields = ()

    def save(self, castle, user, commit=True):
        """Fall sem vistar hverjir eru með hvaða kastala á Watchlist"""
        profile = super(WatchlistCreationForm, self).save(commit=False)
        profile.castle_watch = castle
        profile.user =user
        profile.save()
        return profile