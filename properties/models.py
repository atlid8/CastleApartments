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
    userinfo_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    #Todo offers, address, viewcount
    def __str__(self):
        return self.name

class PropertyImage(models.Model):
    image = models.CharField(max_length=999)
    Property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    def __str__(self):
        return self.property_id.name
