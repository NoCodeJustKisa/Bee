from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from beehive.models import User


class RegistrationForm(UserCreationForm):
    timezone = forms.ChoiceField(choices=User.TIMEZONES_CHOICES, label='Часовой пояс', required=True, widget=forms.Select(attrs={'class': 'dj-form-widget'}))
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'timezone')
