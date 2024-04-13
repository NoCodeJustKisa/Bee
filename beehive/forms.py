from django import forms


class RegistrationForm(forms.Form):
    TIMEZONES = [
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
    username = forms.CharField(label='Имя пользователя', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    timezone = forms.ChoiceField(label='Часовой пояс', choices=TIMEZONES)