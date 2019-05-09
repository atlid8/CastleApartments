from django.db import models

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
    
