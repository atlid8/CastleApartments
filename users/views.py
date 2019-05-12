from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from properties.models import Castle
from users.forms.creationform import UserCreationForm
from users.forms.ProfileForm import ProfileForm, UserEditForm
from users.models import Profile, SearchHistory
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
    context = {'castles' : Castle.objects.filter(verified=False)}
    return render(request, 'front_page/front_page_staff.html', context)

def front_page_admin(request):
    return render(request, 'front_page/front_page_admin.html')

def my_profile(request):
    userid = request.user.id
    return render(request, 'users/my-profile.html', {'castles': Castle.objects.filter(seller_id=userid),
                   })

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
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(instance=profile, data=request.POST)
        form2 = UserEditForm(instance=user, data=request.POST)
        if form.is_valid() and form2.is_valid:
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form2.save()
            return redirect('edit')
    return render(request, 'users/edit.html', {
        'form' : ProfileForm(instance=profile),
        'form2' : UserEditForm(instance=user),
        'profile' : profile,
    })


def my_property(request, id):
    return render(request, 'users/my_property.html',
                  {'castle': get_object_or_404(Castle, pk=id)
                   })


def seller_profile(request, id):
    # TODO: Change from user to profile or similar
    userid = Profile.objects.filter(id=id).first().user_id
    return render(request, 'users/seller_profile.html',
                  {'profile': get_object_or_404(Profile, pk=id),
                   'castles': Castle.objects.filter(seller_id=userid),
                   })

