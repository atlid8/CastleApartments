from django.db import models


class UserInfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    kingdom = models.CharField(max_length=255)


class UserImage(models.Model):
    display_picture = models.CharField(max_length=999)
    userid = models.ForeignKey(UserInfo, on_delete=models.CASCADE)