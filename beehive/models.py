from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Record(models.Model): #снести к чертям
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    mood = models.ForeignKey('Mood', on_delete=models.CASCADE)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)


class Activity(models.Model):
    name = models.CharField(max_length=100)


class Mood(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='moods/')


class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()