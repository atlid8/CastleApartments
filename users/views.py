from django.contrib.auth.models import User
from properties.models import Castle, Watchlist, CastleOffer, SoldCastle
from users.forms.creationform import UserCreationForm
from users.forms.ProfileForm import ProfileForm, UserEditForm
from users.models import Profile, SearchHistory, Notification, Message
from users.forms.notificationform import NotificationForm
from users.forms.message import MessageForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required



# Create your views here.

def about_us(request):
    """Kallar á about us síðuna og tekur við skilaboðum"""
    user = request.user
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/about-us')
    context = {'form': MessageForm(),
               'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)} #Þetta er allstaðar svo notification uppfærist á öllum síðum
    return render(request, 'about_us/about_us.html', context)


def reset_password(request):
    """kallar á reset password síðuna"""
    user = request.user
    if not user.id: #Þetta er til að innskráð fólk fari ekki á þessa síðu
        return render(request, 'users/reset-password.html')
    return redirect("/")

@login_required
def my_profile(request):
    """Síða sem kallar á my-profile"""
    user = request.user
    list_of_watches = []
    watchlist = Watchlist.objects.filter(user_id=user.id)
    for x in watchlist: #Þessi for lúppa er til að fá castle object úr öllum watchlist objectunum
        list_of_watches.append(Castle.objects.filter(id=x.castle_watch_id).first())
    offer_list = CastleOffer.objects.filter(buyer_id=user.id)
    list_of_offers = []
    for x in offer_list:#Þessi for lúppa er til að fá castle object úr öllum castleoffer objectunum
        if Castle.objects.filter(id=x.castle_id).first() not in list_of_offers: #ef að fólk býður oft í sama kastala þá á hann samt bara að koma einu sinni
            list_of_offers.append(Castle.objects.filter(id=x.castle_id).first())
    context = {'castles': Castle.objects.filter(seller_id=user.id),
               'castle_watch': list_of_watches,
               'castle_offer': list_of_offers,
               'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}

    return render(request, 'users/my-profile.html', context)


def register(request):
    """Kallar á síðu til að búa til notanda og býr hann til"""
    if request.user.id: #Til að innskráðir notendur geti ekki farið á þessa síðu
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/login/') #TODO:Check if this is the right path
    return render(request, 'users/register.html', {
        'form': UserCreationForm(),
    })


def edit(request):
    """Kallar á síðu til að breyta notendaupplýsingu og breytir þeim"""
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    if request.method == 'POST':
        form = ProfileForm(instance=profile, data=request.POST)
        form2 = UserEditForm(instance=user, data=request.POST)
        if form.is_valid() and form2.is_valid:
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            form2.save()
            return redirect('/users/'+str(profile.id))
    context = {
            'form' : ProfileForm(instance=profile),
            'form2' : UserEditForm(instance=user),
            'profile' : profile,
            'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
    }
    return render(request, 'users/edit.html', context)


def get_sold_castle(castle):
    soldcastle = SoldCastle()
    soldcastle.name = castle.name
    soldcastle.postcode = castle.postcode
    soldcastle.price = castle.price
    soldcastle.commission = castle.commission
    soldcastle.rooms = castle.rooms
    soldcastle.size = castle.size
    soldcastle.info = castle.info
    soldcastle.street = castle.street
    soldcastle.house_number = castle.house_number
    soldcastle.seller = castle.seller
    soldcastle.id = castle.id
    return soldcastle

def buy_now(request, id):
    """Fall sem að fjarlægir eign af sölu og sendir seljanda og fleirum skilaboð"""
    if not Castle.objects.filter(id=id):
        soldcastle = SoldCastle.objects.filter(id=id).first()
        form = NotificationForm()
        form.save_bought_now_seller(soldcastle, soldcastle.price, user, soldcastle.seller)
        return redirect('/properties/receipt/'+ str(soldcastle.id)')
    castle = get_object_or_404(Castle, pk=id)
    user = request.user
    soldcastle = get_sold_castle(castle)
    soldcastle.buyer = user
    soldcastle.save()
    form = NotificationForm()
    form.save_bought_now_buyer(user, soldcastle)
    form = NotificationForm()
    form.save_bought_now_seller(soldcastle, soldcastle.price, user,soldcastle.seller)
    the_watchlist = Watchlist.objects.filter(castle_watch_id=castle.id)
    for watch in the_watchlist:
        form = NotificationForm()
        watcher = User.objects.filter(id=watch.user_id).first()
        form.save_for_watchlist(soldcastle.buyer, soldcastle, soldcastle.price, watcher)
    the_offer_list = CastleOffer.objects.filter(castle_id = castle.id)
    for watch in the_offer_list:
        form = NotificationForm()
        watcher = User.objects.filter(id=watch.buyer_id).first()
        form.save_for_watchlist(castle, soldcastle.price, watcher)
    castle.delete()
    return redirect('/properties/receipt/'+ str(soldcastle.id))



def accept_offer(request, id):
    offer = get_object_or_404(CastleOffer, pk=id)
    castle = offer.castle
    soldcastle = get_sold_castle(castle)
    soldcastle.buyer = offer.buyer
    soldcastle.price = offer.offer
    soldcastle.commission = offer.offer * 0.1
    soldcastle.save()
    form = NotificationForm()
    form.save_offer_accept(soldcastle, offer.offer, offer.buyer)
    the_watchlist = Watchlist.objects.filter(castle_watch_id=soldcastle.id)
    for watch in the_watchlist:
        form = NotificationForm()
        watcher = User.objects.filter(id=watch.user_id).first()
        form.save_for_watchlist(castle, soldcastle.price, watcher)
    the_offer_list = CastleOffer.objects.filter(castle_id = castle.id)
    for watch in the_offer_list:
        form = NotificationForm()
        watcher = User.objects.filter(id=watch.buyer_id).first()
        form.save_for_watchlist(soldcastle.buyer, soldcastle, offer.offer, watcher)
    castle.delete()
    return redirect('/')

def delete_user(request, id):
    user = User.objects.filter(id=id).first()
    user.delete()
    return redirect('/')


def delete_castle(request, id):
    castle = Castle.objects.filter(id=id).first()
    castle.delete()
    user = request.user
    if user.is_superuser or user.is_staff:
        form = NotificationForm()
        form.save_not_verified(castle)
    return redirect('/')

def delete_search_history(request):
    user = request.user
    search_history = SearchHistory.objects.filter(user_id = user.id)
    for search in search_history:
        search.delete()
    return redirect('/users/search-history')

def verify_castle(request, id):
    castle = Castle.objects.filter(id=id).first()
    castle.verified = True
    castle.save()
    form = NotificationForm()
    form.save_verified(castle)
    return redirect('/')

def read_message(request, id):
    message = Message.objects.filter(id=id).first()
    message.read = True
    message.save()
    return render(request, 'users/single_message.html', {'message': message})


def seller_profile(request, id):
    user = request.user
    # TODO: Change from user to profile or similar
    return render(request, 'users/seller_profile.html',
                  {'profile': get_object_or_404(Profile, pk=id),
                   'castles': Castle.objects.filter(seller_id=Profile.objects.filter(id=id).first().user_id), 'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                   })
@login_required
def search_history(request):
    user = request.user
    userid = request.user.id
    return render(request, 'users/search_history.html',
                  {'histories': SearchHistory.objects.filter(user_id=userid).order_by('-time_stamp'), 'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)})

@login_required
def notification(request):
    userid =request.user
    unseen = Notification.objects.filter(receiver=userid, resolved=False).order_by('-time_stamp')
    seen = Notification.objects.filter(receiver=userid, resolved=True).order_by('-time_stamp')
    for notification in unseen:
        notification.resolved = True
        notification.save()
    return render(request, 'users/notification.html',
                  {'seen': seen,
                   'unseen': unseen})


def messages(request):
    user = request.user
    return render(request, 'users/my-inbox.html', {'messages': Message.objects.all().order_by('-time_stamp'), 'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)})
