from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from properties.models import *
from properties.forms.create import CastleCreationForm, CastleImageCreationForm

# Create your views here.
def index(request):
    return render(request, 'base.html')

def properties(request):
    context = {'castles': Property.objects.all()}
    return render(request, 'properties/properties-index.html', context)

def get_property_by_id(request, id):
    return render(request, 'properties/property_details.html',
                   {'castle' : get_object_or_404(Property, pk=id)
                    })
@login_required
def payments(request):
    return render(request, 'payments/payments.html')

def make_offer(request):
    return render(request, 'payments/make-offer.html')

def create(request):
    if request.method == 'POST':
        form = CastleCreationForm(data=request.POST)
        form2 =CastleImageCreationForm(data=request.POST)
        if form.is_valid():
            if form2.is_valid():
                form.save()
                user_id = User.objects.last()
                postcode = form2['postcode'].value()
                form2.save(user_id, postcode)
                return redirect('dennislog') #TODO:Check if this is the right path
    return render(request, 'properties/create_property.html', {
        'form': CastleCreationForm(),
        'form2': CastleImageCreationForm()
    })

def edit_property(request, id):
    return render(request, 'properties/edit_property.html',
                  {'castle': get_object_or_404(Property, pk=id)
                   })

