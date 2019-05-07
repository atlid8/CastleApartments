from django.shortcuts import render, get_object_or_404
from properties.models import *

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


