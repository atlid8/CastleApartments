from django.db import models
from django.contrib.auth.models import User


class Postcode(models.Model):
    postcode = models.CharField(max_length=255, primary_key=True)
    kingdom = models.CharField(max_length=255)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=9999)
<<<<<<< Updated upstream
=======
    street = models.CharField(max_length=255)
    house_number = models.IntegerField()
    ssn = models.CharField(max_length= 11)

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    postcode = models.ForeignKey(Postcode, on_delete=models.CASCADE, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    house_number = models.IntegerField(blank=True, null=True)
    ssn = models.CharField(max_length= 11,blank=True, null=True)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=9999, blank=True, null=True)

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    searchword = models.CharField(max_length=999)



>>>>>>> Stashed changes
