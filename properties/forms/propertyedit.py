from django.forms import ModelForm
from django.forms import widgets
from django.contrib.auth.models import User
from properties.models import Castle

class CastleEditForm(ModelForm):
    class Meta:
            model = Castle
            exclude = ['id', 'seller', 'commission', 'verified']