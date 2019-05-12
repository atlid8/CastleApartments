from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="base-index"),
    path('search/', views.properties, name="properties-index"),
    path('<int:id>/', views.get_property_by_id, name="property_details"),
    # path('<int:id>/payments/', views.payments, name="payments"),
    # path('<int:id>/make-offer/', views.make_offer, name="make_offer"),
    path('payments/', views.payments, name="payments"),
    path('make-offer/', views.make_offer, name="make_offer"),
    path('create/', views.create, name="create_property"),
    path('<int:id>/edit/', views.edit_property, name="edit_property"),
]