from django.forms import ModelForm
from users.models import Notification, Profile
from properties.models import Castle
from django.contrib.auth.models import User



class NotificationForm(ModelForm):
    """Form sem tekur inn upplýsingar um notification og býr það til"""
    class Meta:
        model = Notification
        exclude = ['receiver', 'id', 'link', 'info', 'time_stamp', 'resolved']

    def save_offer_made(self, buyer, offer, castle, commit=True):
        """Fall sem sendir skilaboð á seljanda um ný tilboð í eign"""
        notification = super(NotificationForm, self).save(commit=False)
        buyername = buyer.first_name + ' ' + buyer.last_name
        castlename = castle.name
        notification.info = buyername + ' just offered ' + str(offer) + ' Gold Dragons for the property: ' + castlename
        castleid = castle.id
        notification.link = '/properties/' + str(castleid)
        notification.resolved = False
        notification.receiver = castle.seller
        notification.save()
        return notification

    def save_reject_offer(self, seller, buyer, castle, price):
        """Fall sem sendir skilaboð á tilboðsgjafa um að tilboði í eign hafi verið hafnað"""
        notification = super(NotificationForm, self).save(commit=False)
        sellername = seller.first_name + ' ' + seller.last_name
        castlename = castle.name
        notification.info = sellername + ' just rejected your offer of ' + str(
            price) + ' Gold Dragons for the property: ' + castlename
        castleid = castle.id
        notification.link = '/properties/' + str(castleid)
        notification.resolved = False
        notification.receiver = buyer
        notification.save()
        return notification
        notification = super(NotificationForm, self).save(commit=False)


    def save_for_watchlist(self, buyer, castle, offer, watcher, commit=True):
        """Fall sem að sendir skilaboð á þa´sem eru með eign á watchlist eða hafa boðið í eign að tilboð hafi verið gert í hana"""
        notification = super(NotificationForm, self).save(commit=False)
        buyername = buyer.first_name + ' ' + buyer.last_name
        castlename = castle.name
        notification.info = buyername + ' just offered ' + str(
            offer) + ' Gold Dragons for the property: ' + castlename
        castleid = castle.id
        notification.link = '/properties/' + str(castleid)
        notification.resolved = False
        notification.receiver = watcher
        notification.save()
        return notification

    def save_for_watchlist_bought(self, buyer, castle, offer, watcher, commit=True):
        """Fall sem að sendir skilaboð á þa´sem eru með eign á watchlist eða hafa boðið í eign að hún hafi verið seld"""
        notification = super(NotificationForm, self).save(commit=False)
        buyername = buyer.first_name + ' ' + buyer.last_name
        castlename = castle.name
        notification.info = buyername + ' just bought the property ' + castlename + ' for ' + str(
            offer) + ' Gold Dragons. You can no longer bid on it.'
        castleid = castle.id
        notification.link = '/properties/' + str(castleid)
        notification.resolved = False
        notification.receiver = watcher
        notification.save()
        return notification


    def save_offer_accept(self, castle, price, buyer):
        """Fall sem sendir skilaboð á tilboðsgjafa um að tilboði hans hafi verið tekið"""
        notification = super(NotificationForm, self).save(commit=False)
        notification.info = 'Your offer of '+ str(price) + ' Gold Dragons for ' + str(castle.name) + ' has been accepted'
        notification.link = '/properties/' +str(castle.id)+ '/contact-info-buy/'
        notification.resolved = False
        notification.receiver = buyer
        notification.save()
        return notification

    def save_bought_now_seller(self, castle, price, buyer, seller):
        """Fall sem sendir skilaboð á seljanda að eign hans hafi verið keypt"""
        notification = super(NotificationForm, self).save(commit=False)
        buyername = buyer.first_name + ' ' + buyer.last_name
        notification.info = buyername + ' just bought your castle ' + str(castle.name) + ' for ' + str(price) + ' Gold Dragons.'
        notification.link = '/properties/receipt/' + str(castle.id)
        notification.resolved = False
        notification.receiver = seller
        notification.save()
        return notification

    def save_bought_now_buyer(self, buyer, castle):
        """Fall sem sendir tilkynningu með kvittun a kaupanda eignar"""
        notification = super(NotificationForm, self).save(commit=False)
        notification.info = 'You just bought ' + str(castle.name) + '! Here is your receipt'
        notification.link = '/properties/receipt/' + str(castle.id)
        notification.resolved = False
        notification.receiver = buyer
        notification.save()
        return notification


    def save_not_verified(self, castle):
        """Fall sem sendir skilaboð á seljanda um að eign hans hafi verið samþykkt"""
        notification = super(NotificationForm, self).save(commit=False)
        notification.receiver = castle.seller
        notification.link = ''
        notification.resolved = False
        notification.info = 'The castle ' + str(castle.name) + ' has been declined'
        notification.save()
        return notification

    def save_verified(self, castle):
        """Fall sem sendir skilaboð á seljanda um að eign hans hafi verið hafnað"""
        notification = super(NotificationForm, self).save(commit=False)
        notification.receiver = castle.seller
        notification.link = '/properties/' + str(castle.id)
        notification.resolved = False
        notification.info = 'The castle ' + str(castle.name) + ' has been verified'
        notification.save()
        return notification

