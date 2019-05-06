from django.db import models


class UserLogIn(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)#TODO


class UserInfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.FloatField(max_length=50)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    username = models.ForeignKey(UserLogIn, on_delete=models.CASCADE)


class UserPicture(models.Model):
    display_picture = models.CharField(max_length=999)
    username = models.ForeignKey(UserInfo, on_delete=models.CASCADE)