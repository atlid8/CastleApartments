from django.db import models
from users.models import User
from users.models import Postcode, Profile
from django.utils import timezone


class SoldCastle(models.Model):
    name = models.CharField(max_length=255)
    postcode = models.ForeignKey(Postcode, on_delete=models.CASCADE)
    price = models.IntegerField()
    commission = models.IntegerField()
    rooms = models.IntegerField()
    size = models.IntegerField()
    info = models.TextField()
    street = models.CharField(max_length=255)
    house_number = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User,related_name='buyer' ,on_delete=models.CASCADE)
    time_stamp=time_stamp = models.DateTimeField(default=timezone.now)


class Castle(models.Model):
    name = models.CharField(max_length=255)
    postcode = models.ForeignKey(Postcode, on_delete=models.CASCADE)
    price = models.IntegerField()
    commission = models.IntegerField()
    rooms = models.IntegerField()
    size = models.IntegerField()
    verified = models.BooleanField()
    info = models.TextField()
    street = models.CharField(max_length=255)
    house_number = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

class CastleImage(models.Model):
    image = models.CharField(max_length=9999)
    castle = models.ForeignKey(Castle, on_delete=models.CASCADE)

class CastleOffer(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    castle = models.ForeignKey(Castle, on_delete=models.CASCADE)
    offer = models.IntegerField()
    info = models.TextField()


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    castle_watch = models.ForeignKey(Castle, on_delete=models.CASCADE)

class ContactInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_name = models.CharField(max_length=255)
    house_number = models.IntegerField()
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.IntegerField()
    ssn = models.IntegerField()

