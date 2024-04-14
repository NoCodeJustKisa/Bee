from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from forms import RegistrationForm
# Create your views here.


def login():
    pass


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():  #надо чота сделать сссс проверкой двух паролей
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            timezone = form.cleaned_data['timezone']
            user = User.objects.create_user(username=username, email=email, password=password, timezone=timezone)
            user.save()
            login(request, user)
            return redirect(' ')  # надо сделать редирект на главную страницу



def logout():
    pass
