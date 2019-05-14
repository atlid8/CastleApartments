from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from properties.models import Castle, Watchlist, CastleOffer, SoldCastle
from users.forms.creationform import UserCreationForm
from users.forms.ProfileForm import ProfileForm, UserEditForm
from users.models import Profile, SearchHistory, Notification
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required



# Create your views here.
def login(request):
    return render(request, 'users/login.html')

def about_us(request):
    return render(request, 'about_us/about_us.html')

def signup(request):
    return render(request, 'users/signup.html')

def reset_password(request):
    return render(request, 'users/reset-password.html')

def front_page_staff(request):
    context = {'castles' : Castle.objects.filter(verified=False)}
    return render(request, 'front_page/front_page_staff.html', context)

def front_page_admin(request):
    return render(request, 'front_page/front_page_admin.html')


@login_required
def my_profile(request):
    userid = request.user.id
    list_of_watches = []
    watchlist = Watchlist.objects.filter(user_id=userid)
    dictionary = {'castles': Castle.objects.filter(seller_id=userid)}
    dictionary['castle_watch'] =[]
    for x in watchlist:
        if Castle.objects.filter(id=x.castle_watch_id).first() not in list_of_watches:
            list_of_watches.append(Castle.objects.filter(id=x.castle_watch_id).first())
    dictionary['castle_watch'] = list_of_watches
    return render(request, 'users/my-profile.html', dictionary)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/login/') #TODO:Check if this is the right path
    return render(request, 'users/register.html', {
        'form': UserCreationForm(),
    })

def profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        print(1)
    return render(request, 'users/notification.html', {
        'form': ''
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
        'profile' : profile,
    })


def my_property(request, id):
    return render(request, 'users/my_property.html',
                  {'castle': get_object_or_404(Castle, pk=id), 'offers': CastleOffer.objects.filter(castle_id=id).order_by('-offer')
                   })

def accept_offer(request, id):
    offer = get_object_or_404(CastleOffer, pk=id)
    soldcastle = SoldCastle()
    soldcastle.name = offer.castle.name
    soldcastle.postcode = offer.castle.postcode
    soldcastle.price = offer.offer
    soldcastle.commission = offer.offer * 0.1
    soldcastle.rooms = offer.castle.rooms
    soldcastle.size = offer.castle.size
    soldcastle.info = offer.castle.info
    soldcastle.street =offer.castle.street
    soldcastle.house_number = offer.castle.house_number
    soldcastle.seller = offer.castle.seller


def seller_profile(request, id):
    # TODO: Change from user to profile or similar
    userid = Profile.objects.filter(id=id).first().user_id
    return render(request, 'users/seller_profile.html',
                  {'profile': get_object_or_404(Profile, pk=id),
                   'castles': Castle.objects.filter(seller_id=userid),
                   })
@login_required
def search_history(request):
    userid = request.user.id


    return render(request, 'users/dennislog.html',
                  {'histories': SearchHistory.objects.filter(user_id=userid).order_by('-time_stamp')})

@login_required
def notification(request):
    userid =request.user
    unseen = Notification.objects.filter(receiver=userid, resolved=False)
    seen = Notification.objects.filter(receiver=userid, resolved=True)
    for notification in unseen:
        notification.resolved = True
        notification.save()
    return render(request, 'users/notification.html',
                  {'seen': seen,
                   'unseen': unseen})


def my_inbox(request):
    return render(request, 'users/my-inbox.html')
