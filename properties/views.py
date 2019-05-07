from django.shortcuts import render
from properties.models import *

# Create your views here.
def index(request):
    return render(request, 'base.html')

def properties(request):
    context = {'castles': Property.objects.all()}
    return render(request, 'properties/properties-index.html', context)




