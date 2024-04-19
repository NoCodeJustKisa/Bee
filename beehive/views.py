from django.shortcuts import render, redirect
import datetime, zoneinfo
from zoneinfo import ZoneInfo
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, CheckinForm
from beehive.models import User as BeehiveUser
from beehive.models import Record
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
    current_user = request.user #берем джанговского юзера
    beehive_user = BeehiveUser.objects.get(username=current_user) #а теперь берем юзера расширенного с тзшкой
    user_timezone = ZoneInfo(beehive_user.timezone) #пихаем строку в ZoneInfo и получаем тз объект с тз пользователя
    current_date = datetime.datetime.now(user_timezone).date() #Получаем че там за день у пользователя сейчас
    records = Record.objects.filter(user=current_user) #берем все записи пользователя
    record = None #тут типа запись которая может и есть а может и нет а может...
    for rec in records: #проходимся по записям (ето ужас канешна полный лицо сервера имаджинируйте :D)
        created_at_user_tz = rec.created_at.astimezone(user_timezone) #переводим время записи в тз пользователя
        if created_at_user_tz.date() == current_date:  #если дата записи равна текущей дате (в тз юзера)
            record = rec #то запись есть и мы ее чпок и выходим из цикла
            break

    if request.method == "POST": # так тут вроде все спокойно никаких всяких ну ты поняла
        form = CheckinForm(request.POST, instance=record) #еси запись имеется то передаем ее еси нет то делаем новую
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('main')
    else:
        if record and record.mood and record.activity:
            # If a record exists for today and both fields are filled, show a message
            return render(request, "checkin.html", context={'message': 'Вы уже отмечались сегодня', 'title': 'Beehive | Отметиться'})
        else:
            # If no record exists or if a record exists but a field is blank, show the form
            form = CheckinForm(instance=record)
    return render(request, "checkin.html", context={'title': 'Beehive | Отметиться', 'form': form})


def home(request):
    return render(request, "home.html", context={'title': 'Beehive | Главная'})
