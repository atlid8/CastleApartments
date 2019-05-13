from django.db import models
from users.models import User
from users.models import Postcode, Profile



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


