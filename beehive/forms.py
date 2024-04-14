from django import forms
from models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    timezone = forms.ChoiceField(label='Часовой пояс', choices=User.TIMEZONES_CHOICES)
