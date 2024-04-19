from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, CheckinForm
# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            # если форма не валидна, то возвращаем ее с ошибками
            return render(request, "registration/register.html", context={'form': form})
    else:
        form = RegistrationForm
    return render(request, "registration/register.html", context={'form': form})


@login_required(redirect_field_name='login')
def mainpage(request):
    if request.method == "POST":
        form = CheckinForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('main')
        else:
            return render(request, "checkin.html", context={'form': form})
    else:
        form = CheckinForm
    return render(request, "checkin.html", context={'title': 'Beehive | Отметиться', 'form': form})


def home(request):
    return render(request, "home.html", context={'title': 'Beehive | Главная'})
