from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class TempUser(models.Model):
    auto_increment_id = models.AutoField(primary_key=True, auto_created=True)
    user = models.CharField(max_length=123)
    password = models.CharField(max_length=120)
    email = models.CharField(max_length=125)
    date = models.DateTimeField()
    code = models.CharField(max_length=198)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "Token of user {}".format(self.user)

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_pic = models.ImageField(default='pic.png')
    email_validate = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return "profile of user {}".format(self.user)

