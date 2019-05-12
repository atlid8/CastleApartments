from django.db import models
from django.contrib.auth.models import User


class Postcode(models.Model):
    postcode = models.CharField(max_length=255, primary_key=True)
    kingdom = models.CharField(max_length=255)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=9999)
