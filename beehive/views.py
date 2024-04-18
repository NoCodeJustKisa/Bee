from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def registration(request):
    pass



def logout():
    pass


@login_required(redirect_field_name='login')
def mainpage(request):
    return render(request, "mother_app.html", context={'title': 'Beehive | Отметиться'})

def home(request):
    return render(request, "home.html", context={'title': 'Beehive | Главная'})
