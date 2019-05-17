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
            return redirect('/users/'+str(profile.id)) #Þetta sendir notandann á prófílinn sem aðrir sjá
    context = {
            'form' : ProfileForm(instance=profile),
            'form2' : UserEditForm(instance=user),
            'profile' : profile,
            'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
    }
    return render(request, 'users/edit.html', context)


def get_sold_castle(castle):
    """Þetta fall tekur upplýsingar um kastala og færir þær í selda kastala"""
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
    """Fall sem að býr til kvittun og sendir seljanda og fleirum skilaboð. Eyðir kastala ef þetta er buy_now"""
    user = request.user
    if not Castle.objects.filter(id=id):#Þetta gerist ef að kaupin eru að gerast í gegnum accept offer. Þá er þegar búið að taka kastalann af sölu
        soldcastle = SoldCastle.objects.filter(id=id).first()
        form = NotificationForm()
        form.save_bought_now_seller(soldcastle, soldcastle.price, user, soldcastle.seller)
        return redirect('/properties/receipt/'+ str(soldcastle.id))
    castle = get_object_or_404(Castle, pk=id)
    soldcastle = get_sold_castle(castle)
    soldcastle.buyer = user
    soldcastle.save()
    form = NotificationForm()
    form.save_bought_now_buyer(user, soldcastle) #sendir kvittun á kaupanda
    form = NotificationForm()
    form.save_bought_now_seller(soldcastle, soldcastle.price, user,soldcastle.seller) #sendir kvittun á seljanda
    send_notifications(soldcastle)
    castle.delete()
    return redirect('/properties/receipt/'+ str(soldcastle.id))


def send_notifications(soldcastle):
    """Sendir notifications á þá sem voru að fylgjast með eða höfðu boðið í kastala"""
    the_watchlist = Watchlist.objects.filter(castle_watch_id=soldcastle.id)
    for watch in the_watchlist:
        form = NotificationForm()
        watcher = User.objects.filter(id=watch.user_id).first()
        if watcher != soldcastle.buyer:#Til að kaupandinn fái ekki mörg notification
            form.save_for_watchlist_bought(soldcastle.buyer, soldcastle, soldcastle.price, watcher)
    the_offer_list = CastleOffer.objects.filter(castle_id=soldcastle.id)
    for watch in the_offer_list:
        form = NotificationForm()
        watcher = User.objects.filter(id=watch.buyer_id).first()
        if watcher != soldcastle.buyer:
            form.save_for_watchlist_bought(soldcastle, soldcastle.price, watcher)


def accept_offer(request, id):
    """Fall sem fjarlægir eign af sölu með því að taka við tilboði"""
    offer = get_object_or_404(CastleOffer, pk=id)
    castle = offer.castle
    soldcastle = get_sold_castle(castle)
    soldcastle.buyer = offer.buyer
    soldcastle.price = offer.offer
    soldcastle.commission = offer.offer * 0.1
    soldcastle.save()
    form = NotificationForm()
    form.save_offer_accept(soldcastle, offer.offer, offer.buyer)
    send_notifications(soldcastle)
    castle.delete()
    return redirect('/')

def delete_user(request, id):
    """Fall sem eyðir notanda"""
    user = User.objects.filter(id=id).first()
    user.delete()
    return redirect('/')


def delete_castle(request, id):
    """Fall sem eyðir kastala"""
    castle = Castle.objects.filter(id=id).first()
    castle.delete()
    user = request.user
    if user.is_superuser or user.is_staff:#Fall sem sendir notification ef einhver annar en notandi eyðir
        form = NotificationForm()
        form.save_not_verified(castle)
    return redirect('/')

def delete_search_history(request):
    """Fall sem eyðir leitarsögu"""
    user = request.user
    search_history = SearchHistory.objects.filter(user_id = user.id)
    for search in search_history:
        search.delete()
    return redirect('/users/search-history')

def verify_castle(request, id):
    """Fall sem að gerir notendum kleift að kaupa fasteign"""
    castle = Castle.objects.filter(id=id).first()
    castle.verified = True
    castle.save()
    form = NotificationForm()
    form.save_verified(castle)
    return redirect('/')

def read_message(request, id):
    """Fall sem merkir skilaboð sem lesin"""
    message = Message.objects.filter(id=id).first()
    message.read = True
    message.save()
    return render(request, 'users/single_message.html', {'message': message})


def seller_profile(request, id):
    """Fall sem sýnir opinberan prófíl notanda. Eingöngu til ef mynd hefur verið sett inn"""
    user = request.user
    context = {'profile': get_object_or_404(Profile, pk=id),
               'castles': Castle.objects.filter(seller_id=Profile.objects.filter(id=id).first().user_id),
               'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                   }
    return render(request, 'users/seller_profile.html',
                 context)

@login_required
def search_history(request):
    """Fall sem kallar á síðu sem sýnir leitarsögu notanda"""
    user = request.user
    context =  {'histories': SearchHistory.objects.filter(user_id=user.id).order_by('-time_stamp'),
                'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
    return render(request, 'users/search_history.html', context
                 )

@login_required
def notification(request):
    """Fall sem kallar á síðu sem sýnir notification notanda"""
    user =request.user
    unseen = Notification.objects.filter(receiver=user.id, resolved=False).order_by('-time_stamp')
    seen = Notification.objects.filter(receiver=user.id, resolved=True).order_by('-time_stamp')
    for notification in unseen:#Breytir öllum óséðum tilkynningum í séðar
        notification.resolved = True
        notification.save()
    context = {'seen': seen,
               'unseen': unseen}
    return render(request, 'users/notification.html', context
                  )


def messages(request):
    """Kallar á síðu sem sínir öll skilaboð sem hafa verið send á starfsmenn"""
    user = request.user
    context =  {'messages': Message.objects.all().order_by('-time_stamp'),
                'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
    return render(request, 'users/my-inbox.html', context)
