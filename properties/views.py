from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from properties.models import *
from users.models import Profile
from properties.forms.create import CastleCreationForm, CastleImageCreationForm
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'base.html')


def properties(request):
    if 'search-filter' in request.GET:
        search_filter = request.GET['search-filter']
        castles = [ {
            'id': x.id,
            'name': x.name,
            'price': x.price,
            'commission': x.commission,
            'rooms': x.rooms,
            'size': x.size,
            'verified' : x.verified,
            'info': x.info,
            'street': x.street,
            'house_number': x.house_number,
            'seller': x.seller.id,
            'firstimage': x.castleimage_set.first().image
        } for x in Castle.objects.filter(name__icontains=search_filter)]
        return JsonResponse({'data': castles})
    context = {'castles': Castle.objects.all().order_by('name')}
    return render(request, 'properties/properties-index.html', context)

def get_property_by_id(request, id):
    return render(request, 'properties/property_details.html',
                   {'castle': get_object_or_404(Castle, pk=id)
                    })

@login_required

def payments(request, id):
    return render(request, 'payments/payments.html',
                  {'castle': get_object_or_404(Castle, pk=id)
                   })

def make_offer(request, id):
    return render(request, 'payments/make-offer.html',
                  {'castle': get_object_or_404(Castle, pk=id)
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
                  {'castle': get_object_or_404(Property, pk=id)
                   })

