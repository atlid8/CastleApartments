from django.db import models
from users.models import User

# Create your models here.
class Property(models.Model):
    name = models.CharField(max_length=255)
    zip = models.IntegerField()
    price = models.IntegerField()
    commission = models.IntegerField()
    rooms = models.IntegerField()
    verified = models.BooleanField()
    info = models.TextField()
    #Todo offers, address, viewcount
    def __str__(self):
        return self.name

class PropertyImage(models.Model):
    image = models.CharField(max_length=999)
    Property = models.ForeignKey(Property, on_delete=models.CASCADE)
    def __str__(self):
        return self.image

class Castle(models.Model):
    name = models.CharField(max_length=255)
    zip = models.IntegerField()
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
    image = models.CharField(max_length=999)
    castle = models.ForeignKey(Castle, on_delete=models.CASCADE)
