from django import forms
from django.contrib.auth.forms import AuthenticationForm
from models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=100, widget=forms.TextInput)
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    timezone = forms.ChoiceField(label='Часовой пояс', choices=User.TIMEZONES_CHOICES, widget=forms.Select)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', max_length=100, widget=forms.TextInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
