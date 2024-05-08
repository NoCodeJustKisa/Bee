from django.shortcuts import render, redirect
import datetime
from datetime import datetime as dt
from zoneinfo import ZoneInfo
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, CheckinForm, NoteForm
from beehive.models import User as BeehiveUser
from beehive.models import Record, Note, Message
import calendar
from .funky import send_to_haiku
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import F, CharField, Avg
from django.db.models.functions import Cast
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
    current_user = request.user
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    beehive_user = BeehiveUser.objects.get(username=current_user)
    user_timezone = ZoneInfo(beehive_user.timezone) #получаем тз объект с тз пользователя
    current_date = datetime.datetime.now(user_timezone).date() #Получаем что за день у пользователя сейчас
    records = Record.objects.filter(user=current_user) #берем все записи пользователя
    record = None
    for rec in records: #проходимся по записям
        created_at_user_tz = rec.created_at.astimezone(user_timezone) #переводим время записи в тз пользователя
        if created_at_user_tz.date() == current_date:  #если дата записи равна текущей дате (в тз юзера)
            record = rec #то запись есть и мы ее сохраняем в record
            break

    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == 'record_form':
            form = CheckinForm(request.POST, instance=record) #Если запись есть, то передаем ее иначе делаем новую
            if form.is_valid(): #валидация
                record = form.save(commit=False)
                record.user = request.user
                record.save()
                return redirect('main')
        elif form_type == 'delete_note_form': # если взаимодействуем с формой удаления заметки
            note_id = request.POST.get('note_id')
            Note.objects.get(id=note_id).delete()
            return redirect('main')
    else:
        if record and record.mood and record.activity:
            # Если запись есть и поля заполнены, то отображаем сообщение
            return render(request, "checkin.html", context={'message': 'Вы уже отмечались сегодня', 'title': 'Beehive | Отметиться', 'notes':notes, 'username':current_user.username})
        else:
            # Если записи нет или одно из полей пустое, то отображаем форму (либо пустую либо с существующей сущностью)
            form = CheckinForm(instance=record)
    return render(request, "checkin.html", context={'title': 'Beehive | Отметиться', 'form': form, 'notes':notes, 'username':current_user.username})


def home(request):
    return render(request, "home.html", context={'title': 'Beehive | Главная'})


@login_required(redirect_field_name='login')
def note_creation(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == "delete_note_form":
            note_id = request.POST.get('note_id')
            Note.objects.get(id=note_id).delete()
            return redirect('createnote')
        else:
            form = NoteForm(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.user = request.user
                note.save()
                return redirect('main')
            else:
                return render(request, "note_creation.html", context={'title': 'Beehive | Создать заметку', 'form': form,'notes':Note.objects.filter(user=request.user), 'username': request.user.username})
    else:
        form = NoteForm()
    return render (request, "note_creation.html", context={'title': 'Beehive | Создать заметку', 'form': form,'notes':Note.objects.filter(user=request.user).order_by('-created_at'), 'username': request.user.username})


@login_required(redirect_field_name='login')
def history(request, year=None, month=None):
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == "delete_note_form":
            note_id = request.POST.get('note_id')
            Note.objects.get(id=note_id).delete()
            return redirect('history')
    else:
        current_user = request.user
        beehive_user = BeehiveUser.objects.get(username=current_user)
        user_timezone = ZoneInfo(beehive_user.timezone)
        now = datetime.datetime.now() #получаем текущее время на сервере
        month = month or now.month #если месяц не передан то берем текущий
        year = year or now.year #если год не передан то берем текущий

        calendarik = calendar.monthcalendar(year, month) #получаем календарь на месяц (по умолчанию текущий)
        records = Record.objects.filter(user = request.user, created_at__year=year, created_at__month=month) #берем все записи пользователя за месяц
        moods = {record.created_at.astimezone(user_timezone).day: record.mood for record in records} #для каждой отметки в отметках создаем местечко в словарике с ключом день (от 1 до 31) и настроением

        for week in calendarik:
            for i, day in enumerate(week):
                if day != 0:
                    week[i] = {'day': day, 'mood': moods.get(day)}
        return render(request, "history.html", context={'title': 'Beehive | История', 'notes':Note.objects.filter(user=request.user).order_by('-created_at'), 'username': request.user.username, 'calendar': calendarik, 'year': year, 'month': month})


@login_required(redirect_field_name='login')
def chat(request):
    messages = Message.objects.filter(user=request.user)
    if request.method == "POST":
        message = request.POST.get('message')
        response = send_to_haiku(message)
        completion = Message(user=request.user, message=message, response=response)
        completion.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chat.html', context={'title': 'Beehive | Чат', 'messages': messages, "username":request.user.username})


@login_required(redirect_field_name='login')
def analytics(request):
    if request.method == "POST":
        start_date = dt.strptime(request.POST.get('start_date'), "%Y-%m-%d") #str to dt
        end_date = dt.strptime(request.POST.get('end_date'), "%Y-%m-%d")
        start_date = start_date.astimezone(ZoneInfo('UTC')) #naive to aware
        end_date = end_date.astimezone(ZoneInfo('UTC'))
        records = Record.objects.filter(user=request.user, created_at__range=(start_date, end_date))
        if not records.exists():
            return render(request, 'analytics.html', context={'title': 'Beehive | Аналитика', 'username': request.user.username, 'message': 'Недостаточно данных :('})
        beehive_user = BeehiveUser.objects.get(username=request.user)
        user_timezone = ZoneInfo(beehive_user.timezone)
        mood_pie = records.values(mood_name=F('mood__name')).annotate(count=Count('id')).order_by('mood_name')
        activity_pie = records.values(activity_name=F('activity__name')).annotate(count=Count('id')).order_by('activity_name')
        mood_line = records.annotate(created_at_str=Cast(F('created_at'), output_field=CharField())).values('created_at_str', 'mood').order_by('created_at')
        bar_graph = records.values(activity_name=F('activity__name')).annotate(avg_mood=Avg('mood')).order_by('activity_name')
        return render(request, 'analytics.html', context={'title': 'Beehive | Аналитика', 'username': request.user.username, 'mood_pie':list(mood_pie),'activity_pie':list(activity_pie),"mood_line":list(mood_line), "bar_graph":list(bar_graph),'charts':True})
    return render(request, 'analytics.html', context={'title': 'Beehive | Аналитика', 'username': request.user.username})
