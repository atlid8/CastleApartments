from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from properties.models import Property
from users.forms.creationform import UserCreationForm, ProfileCreationForm
from users.models import Profile
from django.shortcuts import render, get_object_or_404


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
    return render(request, 'users/profile.html', {
        'form': ''
    })

def edit(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        form2 =ProfileCreationForm(data=request.POST)
        if form.is_valid() and form2.is_valid():
            form.save()
            user_id = User.objects.last()
            postcode = form2['postcode'].value()
            form2.save(user_id, postcode)
            return redirect('/users/login/') #TODO:Check if this is the right path
    return render(request, 'users/edit.html', {
        'form': UserCreationForm(),
        'form2': ProfileCreationForm()
    }),

def my_property(request, id):
    return render(request, 'users/my_property.html',
                  {'castle': get_object_or_404(Property, pk=id)
                   })

