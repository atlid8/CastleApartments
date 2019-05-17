from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from properties.models import *
from properties.models import Watchlist
from users.forms.notification_form import NotificationForm
from users.models import Profile, SearchHistory, Notification
from properties.forms.castle_form import CastleCreationForm, CastleImageCreationForm, CastleEditForm
from properties.forms.watch_list import WatchlistCreationForm
from django.http import JsonResponse
from properties.forms.offer_form import OfferCreationForm
from properties.forms.contact_info_form import ContactInfoCreationForm
from users.forms.user_form import UserCreationForm
from users.models import Message


def index(request):
    """View sem sér um forsíðuna"""
    user = request.user
    if user.is_superuser:#Forsíðan fyrir admin
        if request.method == 'POST':
            form = UserCreationForm(data=request.POST)
            if form.is_valid():
                form.save_staff()
                return redirect('/')
        context = {'staff': User.objects.filter(is_staff=True),
                   'customers': User.objects.filter(is_staff=False),
                   'castles': Castle.objects.all(),
                   'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False),
                   'form': UserCreationForm,}
        return render(request, 'front_page/front_page_admin.html', context)
    if user.is_staff:#Forsíða fyrir starfsmenn
        context = {'castles': Castle.objects.filter(verified=False),
                   'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False),
                   'messages': Message.objects.filter(read=False)}
        return render(request, 'front_page/front_page_staff.html', context)
    return render(request, 'base.html', {'notifications':Notification.objects.filter(receiver_id=user.id, resolved=False)})#Forsíða fyrir aðra


def __search_filter(request, search_filter, castles):
    """Fall sem leitar eftir leitarorðum og vistar í leitarsöguna"""
    user = request.user
    searchhistory = SearchHistory(user=user, search_input=search_filter)
    searchhistory.save()
    return castles.filter(name__icontains=search_filter)


def __search_order(request, order, castles):
    """Fall sem raðar leitarniðurstöðum eftir því sem notandi vill"""
    return castles.all().order_by(order)


def __postcode(request, zip_code, castles):
    """Fall sem að leitar eftir póstnúmeri"""
    if zip_code:
        return castles.filter(postcode_id=zip_code)


def __price_filter(request, price_filter, castles):
    """Fall sem leitar eftir verðbili"""
    price_filter = price_filter.split(',')
    min_val = price_filter[0]
    upper_val = price_filter[1]
    return castles.filter(price__range=(int(min_val), int(upper_val)))


def __square_filter(request, square_filter, castles):
    """Fall sem leitar eftir fermetrafjölda"""
    square_filter = square_filter.split(',')
    min_val = square_filter[0]
    upper_val = square_filter[1]
    return castles.filter(size__range=(int(min_val), int(upper_val)))


def __room_filter(request, room_filter, castles):
    """Fall sem leitar eftir herbergjafjölda"""
    room_filter = room_filter.split(',')
    min_val = room_filter[0]
    upper_val = room_filter[1]
    return castles.filter(rooms__range=(int(min_val), int(upper_val)))


def properties(request):
    """Fall sem sýnir leitarsíðu og kallar á leitarskilyrði"""
    user = request.user
    did_filter = False
    castles = Castle.objects.all()
    if "search_history_link" in request.GET:
        castles = __search_filter(request, request.GET['search-filter'], castles)
        context = {'castles': castles,
                   'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
        return render(request, 'properties/properties_index.html', context)
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
    if did_filter: #Þetta breytir hvað fólk sé miðað við leitarskilyrði
        if castles:
            for x in castles:
                if not Castle.objects.filter(id=x['id']).first().castleimage_set:#Sýnir staðlaða mynd ef það var aldrei sett inn mynd af kastala
                    x['image'] = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'
                elif Castle.objects.filter(id=x['id']).first().castleimage_set.first():#Sýnir fyrstu mynd af kastala
                    x['image'] = Castle.objects.filter(id=x['id']).first().castleimage_set.first().image
                else:#Sýnir staðlaða mynd ef öllum myndum af kastala hefur verið eytt
                    x['image'] = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'
            return JsonResponse({'data': list(castles)})
        else:
            return JsonResponse({'data': list(castles)})
    context = {'castles': Castle.objects.all().order_by('name'),
               'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
    return render(request, 'properties/properties_index.html', context)


def properties_no_search(request):#TODO eyða þessu falli?
    context = {'castles': Castle.objects.filter(name__icontains=request.GET['search-filter']).order_by('name'),
               'notifications': Notification.objects.filter(receiver_id=request.user.id, resolved=False)}
    return render(request, 'properties/properties_index.html', context)


def get_property_by_id(request, id):
    """Fall sem kallar á síðu fyrir einstakar eignir"""
    user = request.user
    castle = get_object_or_404(Castle, pk=id)
    if castle.seller == user: # Þetta sýnir aðra síðu ef seljandi eignar skoðar hana
        context = {'castle': castle,
                    'offers': CastleOffer.objects.filter(castle_id=id).order_by('-offer'),
                    'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                       }
        return render(request, 'users/my_property.html',
                      context)
    if request.method == 'POST':
        form = WatchlistCreationForm(data=request.POST)
        if form.is_valid():
            if Watchlist.objects.filter(castle_watch_id = castle.id, user_id = user.id): #Ef að kastali er þegar á watchlist er honum eytt út
                watchlist_item = Watchlist.objects.filter(castle_watch_id = castle.id, user_id = user.id).first()
                watchlist_item.delete()
            else: #Annars er honum bætt við
                form.save(castle, user)
    context = {'castle': get_object_or_404(Castle, pk=id),
               'watchlist':Watchlist.objects.filter(castle_watch_id = castle.id, user_id = user.id),
               'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                    }
    return render(request, 'properties/property_details.html', context
                   )


@login_required
def contact_info_buy(request, id):
    user = request.user
    if not Castle.objects.filter(id=id): #Þetta eru upplýsingarnar sem þar ef farið er á síðuna í gegnum accept offer
        context = {'castle': SoldCastle.objects.filter(id=id).first(),
                   'form': ContactInfoCreationForm(),
                   'user': user,
                   'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
    else:#Þetta eru upplýsingarnar sem þarf ef farið er á síðun í gegnum buy now
        context = {'castle': get_object_or_404(Castle, pk=id),
                   'form': ContactInfoCreationForm(),
                   'user': user,
                   'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
    if request.method == 'POST':
        form = ContactInfoCreationForm(data=request.POST)
        if form.is_valid():
            form.save(user)
            return redirect('/properties/' + str(id) + '/payment-info/')
    return render(request, 'payments/contact_info_buy.html',
                  context)


def receipt(request, id):
    """FAll sem kallar á síðu sem er með kvittun"""
    user = request.user
    context = {'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False),
               'castle': SoldCastle.objects.filter(id=id).first()}
    return render(request, 'payments/receipt.html',
                  context)


def payments(request, id):#TODO skoða hvort við ættum að taka við einhverjum upplýsingum hér
    """Fall sem kallar á síðu sem lætur notanda skrá inn kortaupplýsingar"""
    user = request.user
    if not ContactInfo.objects.filter(user_id = user.id):#Ef að notandi hefur ekki fyllt út contact info á hann ekki að geta komist hingað
        return redirect('/properties/' + str(id) + '/contact-info-buy')
    if not Castle.objects.filter(id=id):
        context = {'castle': SoldCastle.objects.filter(id=id).first(),
                   'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
    else:
        context = {'castle': get_object_or_404(Castle, pk=id),
                   'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
    return render(request, 'payments/payment_info.html',
                  context)


def review_order(request, id):
    """Fall sem kallar á síðu sem að sýnir kaupanda hvað hann er að fara að kaupa og lætur staðfesta"""
    user = request.user
    if not ContactInfo.objects.filter(user_id = user.id):#Ef að notandi hefur ekki fyllt út contact info á hann ekki að geta komist hingað
        return redirect('/properties/' + str(id) + '/contact-info-buy')
    if not Castle.objects.filter(id=id):
        context = {'castle': SoldCastle.objects.filter(id=id).first(),
                   'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
    else:
        context = {'castle': get_object_or_404(Castle, pk=id),
                    'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
    return render(request, 'payments/review_order.html', context)

def make_offer(request, id):
    """Fall sem kallar á síðu sem gefur notanda möguleika á að gera tilboð í eign"""
    user = request.user
    if request.method == 'POST':
        form = OfferCreationForm(data=request.POST)
        form2 = NotificationForm(data=request.POST)
        if form.is_valid() and form2.is_valid():
            buyer = request.user
            offer = form['offer'].value()#Við þurfum að fá verðið til að geta sent notification
            castle = Castle.objects.filter(id=id).first()
            form.save(buyer, castle)
            form2.save_offer_made(buyer, offer, castle)
            the_watchlist = Watchlist.objects.filter(castle_watch_id = id)
            for watch in the_watchlist:
                form2 = NotificationForm(data=request.POST)
                watcher = User.objects.filter(id=watch.user_id).first()
                if watcher != buyer:#Svo fólk fái ekki notification þegar það býður sjálft í eign
                    form2.save_for_watchlist(buyer, castle, offer, watcher)
            return redirect('/properties/search')
    context = {'castle': get_object_or_404(Castle, pk=id), 'form': OfferCreationForm(),  'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                   }
    return render(request, 'payments/make_offer.html', context
                  )


def create(request):
    """Fall sem kallar á síðu sem að býr til kastala sem þú getur selt"""
    user=request.user
    if not user.id:#Ef fólk er ekki innskráð þá á það ekki að geta selt kastala
        return redirect('/users/register')
    if not Profile.objects.filter(user=request.user).first():#Ef fólk er ekki með prófíl getur það ekki selt kastala
        return redirect('/users/edit')
    if not Profile.objects.filter(user=request.user).first().profile_image:#Ef fólk er ekki með mynd af sér getur það ekki selt kastala
        return redirect('/users/edit')
    if request.method == 'POST':
        form = CastleCreationForm(data=request.POST)
        form2 =CastleImageCreationForm(data=request.POST)
        if form.is_valid() and form2.is_valid():
            seller = Profile.objects.filter(user=request.user).first().user
            verified = False
            postcode = form['postcode'].value()
            commission = int(form['price'].value()) * 0.1
            castle = form.save(seller, verified, postcode, commission)
            form2.save(castle)
            return redirect('/properties/'+str(castle.id))
    context = {
        'form': CastleCreationForm(),
        'form2': CastleImageCreationForm(),
        'profile': Profile.objects.filter(user=request.user).first(),
        'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)}
    return render(request, 'properties/create_property.html', context)


def delete_photo(request, id):
    """Fall sem eyðir mynd af kastala"""
    image = CastleImage.objects.filter(id=id).first()
    castle_id = image.castle.id#Þurfum að taka þetta því við getum ekki vísað í það eftir að við eyðum myndinni
    image.delete()
    return redirect('/properties/' + str(castle_id) + '/photos')


def delete_offer(request, id):
    """FAll sem eyðir tilboði í kastala"""
    offer = CastleOffer.objects.filter(id=id).first()
    castle = offer.castle#Við þurfum að geyma þetta áður en við eyðum offerinu
    notification = NotificationForm()
    notification.save_reject_offer(castle.seller, offer.buyer, castle, offer.offer)
    offer.delete()
    return redirect('/properties/' + str(castle.id))


def edit_property(request, id):
    """FAll sem kallar á síðu sem leyfir okkur að breyta upplýsingum um kastala"""
    user = request.user
    castle = Castle.objects.filter(id=id).first()
    if user != castle.seller:#Þú átt ekki að geta breytt upplýsingum nema að vera notandi
        return redirect('/')
    if request.method == 'POST':
        form = CastleEditForm(instance=castle, data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('/properties/'+ str(castle.id))
    context =  {'castle': get_object_or_404(Castle, pk=id),
                'form': CastleEditForm(instance=castle),
                'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                   }
    return render(request, 'properties/edit_property.html', context
                 )


def edit_photo(request, id):
    """kallar á síðu sem leyfir fólki að eyða eða bæta við myndum"""
    user = request.user
    if request.method == 'POST':
        form = CastleImageCreationForm(data=request.POST)
        if form.is_valid():
            castle = Castle.objects.filter(id=id).first()
            form.save(castle)
            return redirect('/properties/' + str(castle.id) + '/photos')
    context = {'castle_images': CastleImage.objects.filter(castle_id=id),
               'form': CastleImageCreationForm(),
               'notifications': Notification.objects.filter(receiver_id=user.id, resolved=False)
                   }
    return render(request, 'properties/edit_photo.html', context)