from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Postcode(models.Model):
    postcode = models.CharField(max_length=255, primary_key=True)
    kingdom = models.CharField(max_length=255)

    def __str__(self):
        return str(self.postcode)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=9999)

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_input = models.CharField(max_length=999)
    time_stamp = models.DateTimeField(default=timezone.now)

class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.CharField(max_length=999)
    link = models.CharField(max_length=255)
    resolved = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(default=timezone.now)

class Countries(models.Model):
    country = models.CharField(max_length=255)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    time_stamp = models.DateTimeField(default=timezone.now)


