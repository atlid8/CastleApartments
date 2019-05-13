from django.forms import ModelForm
from users.models import Notification, Profile
from properties.models import Castle
from django.contrib.auth.models import User



class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        exclude = ['receiver', 'id', 'link', 'info', 'time_stamp', 'resolved']



    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


    def save_offer_made(self, buyer, offer, castle, commit=True):
        notification = super(NotificationForm, self).save(commit=False)
        buyername = buyer.first_name + ' ' + buyer.last_name
        castlename = castle.name
        notification.info = buyername + ' just offered ' + str(offer) + ' for the property:' + castlename
        notification.link =


    def save_for_watchlist(self, castle, watchlistid, commit=True):
        pass

    def save_counteroffer(self, castle, ):
        pass



    def save_message_notification(self, receiver, sender, info, commit=True):
        pass
