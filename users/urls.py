from . import views
from django.urls import path

urlpatterns = [
    path('', views.login, name="login-page"),
    path('about-us/', views.about_us, name="about-us"),
]
