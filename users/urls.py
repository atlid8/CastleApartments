from . import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', views.login, name="login-page"),
    path('about-us/', views.about_us, name='about-us'),
    path('sign-up/', views.signup, name='sign-up'),
    path('password-reset/', views.reset_password, name='password-reset'),
    path('staff/', views.front_page_staff, name='front-page-staff'),
    path('my-profile/', views.my_profile, name='password-reset'),
    path('admin/', views.front_page_admin, name='front-page-admin'),
    path('register/', views.register, name='register'),
    path('dennislog', LoginView.as_view(template_name= 'users/dennislog.html'), name='dennislog'),
    path('logout', LogoutView.as_view(next_page='dennislog'), name='logout'), #TODO: breyta next page ef ekki virkar
]
