from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Postcode(models.Model):
    postcode = models.CharField(max_length=255, primary_key=True)
    kingdom = models.CharField(max_length=255)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=9999)

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_input = models.CharField(max_length=999)
    time_stamp = models.DateTimeField(default=timezone.now)
