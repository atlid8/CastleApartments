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
    user = request.user
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/about-us')
    context = {'form': MessageForm(),
               'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False) }
    return render(request, 'about_us/about_us.html', context)


def reset_password(request):
    user = request.user
    if not user.id:
        return render(request, 'users/reset-password.html')
    return redirect("/")

@login_required
def my_profile(request):
    user = request.user
    offer_list = CastleOffer.objects.filter(buyer_id=user.id)
    list_of_offers = []
    for x in offer_list:
        if Castle.objects.filter(id=x.castle_id).first() not in list_of_offers:
            list_of_offers.append(Castle.objects.filter(id=x.castle_id).first())
    context = {'castle_offer': list_of_offers,
               'castles': Castle.objects.filter(seller_id=user.id),
               'castle_watch': Watchlist.objects.filter(user_id=user.id),
               'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
    return render(request, 'users/my-profile.html', context)


def front_page_admin(request): #TODO eyða ef hitt virkar jafn vel
    user = request.user
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save_staff()
            return redirect('/') #TODO:Check if this is the right path
    context = {'staff': User.objects.filter(is_staff=True), 'customers':User.objects.filter(is_staff=False),
               'castles': Castle.objects.all(), 'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False), 'form': UserCreationForm}
    return render(request, 'front_page/front_page_admin.html', context)


def register(request):
    if request.user.id:
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
    profile = Profile.objects.filter(user=request.user).first()
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(instance=profile, data=request.POST)
        form2 = UserEditForm(instance=user, data=request.POST)
        if form.is_valid() and form2.is_valid:
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form2.save()
            return redirect('edit')
    return render(request, 'users/edit.html', {
        'form' : ProfileForm(instance=profile),
        'form2' : UserEditForm(instance=user),
        'profile' : profile, 'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
    })


def buy_now(request, id):
    if not Castle.objects.filter(id=id):
        return redirect('/')
    castle = get_object_or_404(Castle, pk=id)
    user = request.user
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
    soldcastle.buyer = user
    soldcastle.id = castle.id
    soldcastle.save()
    form = NotificationForm()
    form.save_bought_now_buyer(user, soldcastle)
    form = NotificationForm()
    form.save_bought_now_seller(soldcastle, soldcastle.price, user,soldcastle.seller)
    the_watchlist = Watchlist.objects.filter(castle_watch_id=castle.id)
    for watch in the_watchlist: #TODO checka hvort þetta fari ekki inn í forlúppuna þegar
        form = NotificationForm()
        watcher = User.objects.filter(id=watch.user_id).first()
        form.save_for_watchlist(castle, offer.offer, watcher)
    the_offer_list = CastleOffer.objects.filter(castle_id = castle.id)
    for watch in the_offer_list: #Todo checka hvort þetta fari ekki í forlúppuna
        form = NotificationForm()
        watcher = User.objects.filter(id=watch.buyer_id).first()
        form.save_for_watchlist(castle, offer.offer, watcher)
    castle.delete()
    return redirect('/properties/receipt/'+ str(soldcastle.id))

def accept_offer(request, id):
    offer = get_object_or_404(CastleOffer, pk=id)
    castle = offer.castle
    soldcastle = SoldCastle()
    soldcastle.name = castle.name
    soldcastle.postcode = castle.postcode
    soldcastle.price = offer.offer
    soldcastle.commission = offer.offer * 0.1
    soldcastle.rooms = castle.rooms
    soldcastle.size = castle.size
    soldcastle.info = castle.info
    soldcastle.street = castle.street
    soldcastle.house_number = castle.house_number
    soldcastle.seller = castle.seller
    soldcastle.buyer = offer.buyer
    soldcastle.id = castle.id
    soldcastle.save()
    castle.delete()
    form = NotificationForm()
    form.save_offer_accept(soldcastle, offer.offer, offer.buyer)
    the_watchlist = Watchlist.objects.filter(castle_watch_id=castle.id)
    for watch in the_watchlist: #TODO checka hvort þetta fari ekki inn í forlúppuna þegar
        form = NotificationForm()
        watcher = User.objects.filter(id=watch.user_id).first()
        form.save_for_watchlist(castle, offer.offer, watcher)
    the_offer_list = CastleOffer.objects.filter(castle_id = castle.id)
    for watch in the_offer_list: #Todo checka hvort þetta fari ekki í forlúppuna
        form = NotificationForm()
        watcher = User.objects.filter(id=watch.buyer_id).first()
        form.save_for_watchlist(castle, offer.offer, watcher)
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
