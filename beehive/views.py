from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
# Create your views here.


def registration(request):
    pass



def logout():
    pass


def mainpage(request):
    return render(request, "mother_app.html", context={'title': 'Beehive | Отметиться'})

def home(request):
    return render(request, "home.html", context={'title': 'Beehive | Главная'})
