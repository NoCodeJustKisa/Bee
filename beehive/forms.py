from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from beehive.models import User, Record, Mood, Activity, Note
from django.forms import ModelChoiceField, RadioSelect


class RegistrationForm(UserCreationForm):
    timezone = forms.ChoiceField(choices=User.TIMEZONES_CHOICES, label='Часовой пояс', required=True, widget=forms.Select(attrs={'class': 'dj-form-widget'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'timezone')


class CheckinForm(forms.ModelForm):
    mood = ModelChoiceField(queryset=Mood.objects.all(), required=False, widget=forms.RadioSelect())
    activity = ModelChoiceField(queryset=Activity.objects.all(), required=False, widget=forms.RadioSelect())

    class Meta:
        model = Record
        fields = ('mood', 'activity')

    def clean_mora(self):
        cleaned_data = super().clean()
        mood = cleaned_data.get('mood')
        activity = cleaned_data.get('activity')
        if mood is None and activity is None:
            raise forms.ValidationError('Вы не можете ничего не отметить')

    def clean(self): #вызываем clean_mora чтобы была кастомная валидация c проверкой на заполнение хотя бы одного поля
        cleaned_data = super().clean()
        self.clean_mora()
        return cleaned_data


class NoteForm(forms.ModelForm):
    text = forms.CharField(label=" ", widget=forms.Textarea(attrs={'class': 'dj-note-widget'}))

    class Meta:
        model = Note
        fields = ('text',)
