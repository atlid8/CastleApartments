from django.forms import ModelForm
from users.models import Notification, Profile
from properties.models import Castle
from django.contrib.auth.models import User



class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        exclude = ['receiver', 'id', 'link', 'info', 'time_stamp', 'resolved']






    def save_offer_made(self, buyer, offer, castle, commit=True):
        notification = super(NotificationForm, self).save(commit=False)
        buyername = buyer.first_name + ' ' + buyer.last_name
        castlename = castle.name
        notification.info = buyername + ' just offered ' + str(offer) + ' Golden Dragons for the property: ' + castlename
        castleid = castle.id
        notification.link = '/users/my-properties/' + str(castleid)
        notification.resolved = False
        notification.receiver = castle.seller
        notification.save()
        return notification


    def save_for_watchlist(self, buyer, castle, offer, watcher, commit=True):
        """notification = super(NotificationForm, self).save(commit=False)
        buyername = buyer.first_name + ' ' + buyer.last_name
        castlename = castle.name
        notification.info = buyername + ' just offered ' + str(
            offer) + ' Golden Dragons for the property: ' + castlename
        castleid = castle.id
        notification.link = '/properties/' + str(castleid)
        notification.resolved = False
        notification.receiver = watcher
        notification.save()
        return notification"""
        # Þetta virkar en þetta over writar alltaf notificationið á undan
        pass #TODO: Gera watchlist notification

    def save_counteroffer(self, castle, ):
        pass #TODO: Gera counteroffer notification


    def save_message_notification(self, receiver, sender, info, commit=True):
        pass #TODO: Gera message notification
