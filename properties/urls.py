from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="base-index"),
    path('search/', views.properties, name="properties-index"),
    path('<int:id>/', views.get_property_by_id, name="property_details"),
    path('<int:id>/checkout/', views.payments, name="payments"),
    path('<int:id>/make-offer/', views.make_offer, name="make_offer"),
    path('create/', views.create, name="create_property"),
    path('<int:id>/edit/', views.edit_property, name="edit_property"),
    path('<int:id>/contact-info-buy/', views.contact_info_buy, name="contact_info_buy"),
    path('<int:id>/contact-info-offer/', views.contact_info_offer, name="contact_info_offer"),
    path('<int:id>/photos', views.edit_photo, name="edit_photo"),
    path('delete_photo/<int:id>', views.delete_photo, name="delete_photo"),
]