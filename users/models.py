from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Postcode(models.Model):
    """Klasi sem heldur utan um hvaða póstnúmer eru í hvaða konungsríki"""
    postcode = models.CharField(max_length=255, primary_key=True)
    kingdom = models.CharField(max_length=255)

    def __str__(self):
        return str(self.postcode)

class Profile(models.Model):
    """Klasi sem heldur utan um prófíl tengdan við notanda"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=9999)

class SearchHistory(models.Model):
    """klasi sem heldur utan um leitarsögu notanda"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_input = models.CharField(max_length=999)
    time_stamp = models.DateTimeField(default=timezone.now)

class Notification(models.Model):
    """klasi sem heldur utan um tilkynningar til notanda"""
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.CharField(max_length=999)
    link = models.CharField(max_length=255)
    resolved = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(default=timezone.now)

class Countries(models.Model):
    """klasi sem heldur utan um öll lönd í heiminum"""
    country = models.CharField(max_length=255)

class Message(models.Model):
    """Klasi sem heldur utan um skilaboð til starfsmanna"""
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    time_stamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)


