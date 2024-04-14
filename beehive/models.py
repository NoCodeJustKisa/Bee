from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    TIMEZONES_CHOICES = [
        ('Europe/Kaliningrad', 'Калининград'),
        ('Europe/Moscow', 'Москва'),
        ('Europe/Samara', 'Самара'),
        ('Asia/Yekaterinburg', 'Екатеринбург'),
        ('Asia/Omsk', 'Омск'),
        ('Asia/Krasnoyarsk', 'Красноярск'),
        ('Asia/Irkutsk', 'Иркутск'),
        ('Asia/Yakutsk', 'Якутск'),
        ('Asia/Magadan', 'Магадан'),
        ('Asia/Kamchatka', 'Камчатка'),
        ('UTC', 'UTC'),
    ]
    timezone = models.CharField(max_length=64, choices=TIMEZONES_CHOICES, default='UTC')


class Activity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=255, blank=True, null=True)  # путь к иконке в статике


class Mood(models.Model):
    name = models.CharField(max_length=100)
    rate = models.IntegerField()
    icon = models.CharField(max_length=255, blank=True, null=True)  # путь к иконке в статике


class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()  # сообщение пользователя к ллм
    response = models.TextField()  # ответ ллм
    created_at = models.DateTimeField(auto_now_add=True)


class Record(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='records')
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE, blank=True, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
