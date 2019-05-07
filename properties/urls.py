from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="base-index"),
    path('properties/', views.properties, name="properties-index"),
]
