from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from properties.models import *
from users.forms.notificationform import NotificationForm
from users.models import Profile, SearchHistory, Notification
from properties.forms.create import CastleCreationForm, CastleImageCreationForm
from properties.forms.watchlist import WatchlistCreationForm
from django.http import JsonResponse
from properties.forms.offer import OfferCreationForm
from properties.forms.contactinfo import ContactInfoCreationForm


def index(request):
    return render(request, 'base.html')


def properties(request):
    if 'search-filter' in request.GET:
        search_filter = request.GET['search-filter']
        user = request.user
        searchhistory = SearchHistory(user=user, search_input=search_filter)
        searchhistory.save()
        castles = Castle.objects.filter(name__icontains=search_filter).values()
        for x in castles:
            x['image'] = Castle.objects.filter(id=x['id']).first().castleimage_set.first().image
        return JsonResponse({'data': list(castles)})
    if 'order' in request.GET:
        order_by = request.GET['order']
        castles = Castle.objects.all().order_by(order_by).values()
        for x in castles:
            x['image'] = Castle.objects.filter(id=x['id']).first().castleimage_set.first().image
        return JsonResponse({'data': list(castles)})
    context = {'castles': Castle.objects.all().order_by('name')}
    return render(request, 'properties/properties-index.html', context)

def get_property_by_id(request, id):
    if request.method == 'POST':
        form = WatchlistCreationForm(data=request.POST)
        if form.is_valid():
            castle = Castle.objects.filter(id=id).first()
            user = request.user
            form.save(castle, user)
    return render(request, 'properties/property_details.html',
                   {'castle': get_object_or_404(Castle, pk=id)
                    })

@login_required

def contact_info(request, id):
    user = request.user
    if request.method == 'POST':
        form = ContactInfoCreationForm(data=request.POST)
        if form.is_valid():
            form.save(user)
            return redirect('/properties/' + str(id) + '/checkout/')
    return render(request, 'payments/contact-info.html',
                  {'castle': get_object_or_404(Castle, pk=id), 'form': ContactInfoCreationForm(), 'user': user})

def payments(request, id):
    return render(request, 'payments/payments.html',
                  {'castle': get_object_or_404(Castle, pk=id)
                   })

def make_offer(request, id):
    if request.method == 'POST':
        form = OfferCreationForm(data=request.POST)
        form2 = NotificationForm(data=request.POST)
        if form.is_valid() and form2.is_valid():
            buyer = request.user
            offer = form['offer'].value()
            castle = Castle.objects.filter(id=id).first()
            form.save(buyer, castle)
            form2.save(buyer, offer, castle)
            return redirect('/properties/'+str(id)+'/checkout/')
    return render(request, 'payments/make-offer.html',
                  {'castle': get_object_or_404(Castle, pk=id), 'form': OfferCreationForm()
                   })

def create(request):
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
        'profile': Profile.objects.filter(user=request.user).first()
    })

def edit_property(request, id):
    return render(request, 'properties/edit_property.html',
                  {'castle': get_object_or_404(Castle, pk=id)
                   })
