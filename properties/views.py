from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from properties.models import *
from properties.models import Watchlist
from users.forms.notificationform import NotificationForm
from users.models import Profile, SearchHistory, Notification
from properties.forms.create import CastleCreationForm, CastleImageCreationForm
from properties.forms.watchlist import WatchlistCreationForm
from django.http import JsonResponse
from properties.forms.offer import OfferCreationForm
from properties.forms.contactinfo import ContactInfoCreationForm
from properties.forms.propertyedit import CastleEditForm
from users import views


def index(request):
    user = request.user
    return render(request, 'base.html', {'notifications':Notification.objects.filter(receiver_id=user.id, resolved=False)})


def __search_filter(request, search_filter, castles):
    user = request.user
    searchhistory = SearchHistory(user=user, search_input=search_filter)
    searchhistory.save()
    return castles.filter(name__icontains=search_filter)


def __search_order(request, order, castles):
    return castles.all().order_by(order)


def __postcode(request, zip_code, castles):
    if zip_code:
        return castles.filter(postcode_id=zip_code)


def __price_filter(request, price_filter, castles):
    price_filter = price_filter.split(',')
    min_val = price_filter[0]
    upper_val = price_filter[1]
    return castles.filter(price__range=(int(min_val), int(upper_val)))


def __square_filter(request, square_filter, castles):
    square_filter = square_filter.split(',')
    min_val = square_filter[0]
    upper_val = square_filter[1]
    return castles.filter(size__range=(int(min_val), int(upper_val)))


def __room_filter(request, room_filter, castles):
    room_filter = room_filter.split(',')
    min_val = room_filter[0]
    upper_val = room_filter[1]
    return castles.filter(rooms__range=(int(min_val), int(upper_val)))


def properties(request):
    user = request.user
    did_filter = False
    castles = Castle.objects.all()
    if 'search-filter' in request.GET:
        did_filter = True
        castles = __search_filter(request, request.GET['search-filter'], castles)
    if 'order' in request.GET:
        did_filter = True
        castles = __search_order(request, request.GET["order"], castles)
    if 'postcode' in request.GET:
        did_filter = True
        castles = __postcode(request, request.GET['postcode'], castles)
    if 'price-filter' in request.GET:
        did_filter = True
        castles = __price_filter(request, request.GET['price-filter'], castles)
    if 'square-filter' in request.GET:
        did_filter = True
        castles = __square_filter(request, request.GET['square-filter'], castles)
    if 'room-filter' in request.GET:
        did_filter = True
        castles = __room_filter(request, request.GET['room-filter'], castles)
    castles = castles.values()
    if did_filter:
        if castles:
            for x in castles:
                if not Castle.objects.filter(id=x['id']).first().castleimage_set:
                    x['image'] = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'
                elif Castle.objects.filter(id=x['id']).first().castleimage_set.first():
                    x['image'] = Castle.objects.filter(id=x['id']).first().castleimage_set.first().image
                else:
                    x['image'] = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'
            return JsonResponse({'data': list(castles)})
        else:
            return JsonResponse({'data': list(castles)})
    context = {'castles': Castle.objects.all().order_by('name'), 'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
    return render(request, 'properties/properties-index.html', context)


def get_property_by_id(request, id):
    user = request.user
    castle = Castle.objects.filter(id=id).first()
    if castle.seller == user:
        return render(request, 'users/my_property.html',
                      {'castle': get_object_or_404(Castle, pk=id),
                       'offers': CastleOffer.objects.filter(castle_id=id).order_by('-offer'),  'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                       })
    if request.method == 'POST':
        form = WatchlistCreationForm(data=request.POST)
        if form.is_valid():
            if Watchlist.objects.filter(castle_watch_id = castle.id, user_id = user.id):
                watchlist_item = Watchlist.objects.filter(castle_watch_id = castle.id, user_id = user.id).first()
                watchlist_item.delete()
            else:
                form.save(castle, user)
    return render(request, 'properties/property_details.html',
                   {'castle': get_object_or_404(Castle, pk=id), 'watchlist':Watchlist.objects.filter

                   (castle_watch_id = castle.id, user_id = user.id),  'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                    })



@login_required
def contact_info_buy(request, id):
    user = request.user
    if request.method == 'POST':
        form = ContactInfoCreationForm(data=request.POST)
        if form.is_valid():
            form.save(user)
            return redirect('/properties/' + str(id) + '/checkout/')
    return render(request, 'payments/contact-info-buy.html',
                  {'castle': get_object_or_404(Castle, pk=id), 'form': ContactInfoCreationForm(), 'user': user,  'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)})


@login_required
def contact_info_offer(request, id):
    user = request.user
    if request.method == 'POST':
        form = ContactInfoCreationForm(data=request.POST)
        if form.is_valid():
            form.save(user)
            return redirect('/properties/' + str(id) + '/make-offer/')
    return render(request, 'payments/contact-info-offer.html',
                  {'castle': get_object_or_404(Castle, pk=id), 'form': ContactInfoCreationForm(), 'user': user,  'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)})

def payments(request, id):
    user = request.user
    return render(request, 'payments/payments.html',
                  {'castle': get_object_or_404(Castle, pk=id),  'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                   })

def make_offer(request, id):
    user = request.user
    if request.method == 'POST':
        form = OfferCreationForm(data=request.POST)
        form2 = NotificationForm(data=request.POST)
        if form.is_valid() and form2.is_valid():
            buyer = request.user
            offer = form['offer'].value()
            castle = Castle.objects.filter(id=id).first()
            form.save(buyer, castle)
            form2.save_offer_made(buyer, offer, castle)
            the_watchlist = Watchlist.objects.filter(castle_watch_id = id)
            for watch in the_watchlist:
                form2 = NotificationForm(data=request.POST)
                watcher = User.objects.filter(id=watch.user_id).first()
                form2.save_for_watchlist(buyer, castle, offer, watcher)
            #Todo að fá þetta til að hætta að overwrita síðasta form2 save
            return redirect('/properties/'+str(id)+'/checkout/')
    return render(request, 'payments/make-offer.html',
                  {'castle': get_object_or_404(Castle, pk=id), 'form': OfferCreationForm(),  'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                   })

def create(request):
    user=request.user
    if not Profile.objects.filter(user=request.user).first():
        return redirect('/users/edit')
    if not Profile.objects.filter(user=request.user).first().profile_image:
        return redirect('/users/edit')
    if request.method == 'POST':
        form = CastleCreationForm(data=request.POST)
        form2 =CastleImageCreationForm(data=request.POST)
        if form.is_valid() and form2.is_valid():
            seller = Profile.objects.filter(user=request.user).first().user
            verified = False
            postcode = form['postcode'].value()
            commission = int(form['price'].value()) * 0.1
            form.save(seller, verified, postcode, commission)
            the_castle = Castle.objects.last()
            form2.save(the_castle)
            castleid = str(Castle.objects.last().id)
            return redirect('/') #TODO:Check if this is the right path
    return render(request, 'properties/create_property.html', {
        'form': CastleCreationForm(),
        'form2': CastleImageCreationForm(),
        'profile': Profile.objects.filter(user=request.user).first(),  'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
    })

def delete_photo(request, id):
    image = CastleImage.objects.filter(id=id).first()
    castle_id = image.castle.id
    image.delete()
    return redirect('/properties/' + str(castle_id) + '/photos')

def edit_property(request, id):
    user = request.user
    castle = Castle.objects.filter(id=id).first()
    if request.method == 'POST':
        form = CastleEditForm(instance=castle, data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('/properties/'+ str(castle.id))
    return render(request, 'properties/edit_property.html',
                  {'castle': get_object_or_404(Castle, pk=id),
                   'form': CastleEditForm(instance=castle),  'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                   })



def edit_photo(request, id):
    user = request.user
    if request.method == 'POST':
        form = CastleImageCreationForm(data=request.POST)
        if form.is_valid():
            castle = Castle.objects.filter(id=id).first()
            form.save(castle)
            return redirect('/properties/' + str(castle.id) + '/photos')
    return render(request, 'properties/edit_photo.html',{'castle_images': CastleImage.objects.filter(castle_id=id),
                   'form': CastleImageCreationForm(),  'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                   })