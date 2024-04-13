from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    timezone = models.CharField(max_length=64, default='UTC')


class Activity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=255)  # путь к иконке в статике


class Mood(models.Model):
    name = models.CharField(max_length=100)
    rate = models.IntegerField()
    icon = models.CharField(max_length=255)  # путь к иконке в статике


class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()  # сообщение пользователя к ллм
    response = models.TextField()  # ответ ллм
    created_at = models.DateTimeField(auto_now_add=True)


class Record(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='records')
    created_at = models.DateTimeField(auto_now_add=True)
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
