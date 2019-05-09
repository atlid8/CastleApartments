from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="base-index"),
    path('search', views.properties, name="properties-index"),
    path('<int:id>', views.get_property_by_id, name="property_details"),
    path('payments/', views.payments, name="payments"),
    path('create/', views.create, name="create_property")
]