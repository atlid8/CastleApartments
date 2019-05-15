from django import forms
from django.forms import ModelForm
from django.forms import widgets
from users.models import Message

class MessageForm(ModelForm):
    class Meta:
            model = Message
            exclude = ['id', 'time_stamp']
