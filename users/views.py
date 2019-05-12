from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from properties.models import Property
from users.forms.creationform import UserCreationForm
from users.forms.ProfileForm import ProfileForm
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
    profile = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('edit')
    return render(request, 'users/edit.html', {
        'form' : ProfileForm(instance=profile),
        'profile' : profile,
    })


def my_property(request, id):
    return render(request, 'users/my_property.html',
                  {'castle': get_object_or_404(Property, pk=id)
                   })


def seller_profile(request, id):
    # TODO: Change from user to profile or similar
    return render(request, 'users/seller_profile.html',
                  {'user': get_object_or_404(User, pk=id)
                   })
