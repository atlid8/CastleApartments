from . import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(template_name= 'users/login.html'), name='login-page'),
    path('about-us/', views.about_us, name='about-us'),
    path('sign-up/', views.signup, name='sign-up'),
    path('password-reset/', views.reset_password, name='password-reset'),
    path('staff/', views.front_page_staff, name='front-page-staff'),
    path('my-profile/', views.my_profile, name='my-profile'),
    path('admin/', views.front_page_admin, name='front-page-admin'),
    path('register/', views.register, name='register'),
    path('dennislog/', views.search_history, name='dennislog'), #TODO: breyta nafni
    path('logout', LogoutView.as_view(next_page='login/'), name='logout'), #TODO: breyta next page ef ekki virkar
    path('my-properties/<int:id>/', views.my_property, name="edit_property"),
    path('edit/', views.edit, name="edit"),
    path('<int:id>/', views.seller_profile, name="seller_profile"),
    path('notifications/', views.notification, name="notifications"),
    path('my-inbox/', views.my_inbox, name="my-inbox")

]
