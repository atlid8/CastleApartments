from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="base-index"),
    path('properties/', views.properties, name="properties-index"),
    path('properties/<int:id>', views.get_property_by_id, name="property_details"),
    path('payments/', views.payments, name="payments"),
]