from django.shortcuts import render
from properties.models import Property

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
    context = {'castles' : Property.objects.filter(verified=False)}
    return render(request, 'front_page/front_page_staff.html', context)

def front_page_admin(request):
    return render(request, 'front_page/front_page_admin.html')

def my_profile(request):
    context = {'castles': Property.objects.all()}
    return render(request, 'users/my-profile.html', context)