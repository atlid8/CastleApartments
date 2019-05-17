from . import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/log_in.html'), name='login-page'),
    path('about-us/', views.about_us, name='about-us'),
    path('password-reset/', views.reset_password, name='password-reset'),
    path('my-profile/', views.my_profile, name='my-profile'),
    path('register/', views.register, name='register'),
    path('search-history/', views.search_history, name='search-history'),
    path('logout', LogoutView.as_view(next_page='login/'), name='logout'), #TODO: breyta next page ef ekki virkar
    #path('my-properties/<int:id>/', views.my_property, name="edit_property"),
    path('edit/', views.edit, name="edit"),
    path('<int:id>/', views.seller_profile, name="seller_profile"),
    path('notifications/', views.notification, name="notifications"),
    path('messages/', views.messages, name="my-inbox"),
    path('accept_offer/<int:id>', views.accept_offer, name="accept"),
    path('delete_castle/<int:id>', views.delete_castle, name="delete_castle"),
    path('verify_castle/<int:id>', views.verify_castle, name="verify_castle"),
    path('messages/<int:id>', views.read_message, name="read_message"),
    path('delete_user/<int:id>', views.delete_user, name="delete_user"),
    path('delete_search_history', views.delete_search_history, name="delete_search"),
    path('buy_now/<int:id>', views.buy_now, name="buy_now"),

]
