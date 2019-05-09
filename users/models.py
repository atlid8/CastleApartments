from django.db import models
from django.contrib.auth.models import User


class Zip(models.Model):
    Zip = models.IntegerField(primary_key=True)
    kingdom = models.CharField(max_length=255)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zip =models.ForeignKey(Zip, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=9999)
    street = models.CharField(max_length=255)
    house_number = models.IntegerField()
    ssn = models.CharField(max_length= 11)


