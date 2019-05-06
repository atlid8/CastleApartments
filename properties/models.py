from django.db import models
from users.models import UserInfo

# Create your models here.
class Property(models.Model):
    name = models.CharField(max_length=255)
    zip = models.IntegerField()
    price = models.IntegerField()
    commission = models.IntegerField()
    rooms = models.IntegerField()
    verified = models.BooleanField()
    sellerID = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    #Todo offers, address, viewcount
    def __str__(self):
        return self.name

class propertyImage(models.Model):
    image = models.CharField(max_length=999)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)