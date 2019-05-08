from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login, name="login-page"),
    path('about-us/', views.about_us, name='about-us'),
    path('sign-up/', views.signup, name='sign-up'),
    path('password-reset/', views.reset_password, name='password-reset'),
    path('', views.front_page, name='front-page')
]
