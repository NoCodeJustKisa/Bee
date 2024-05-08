import pytest
from django.test import Client, TestCase
from beehive.models import Record, Note, Message, Mood, Activity
from zoneinfo import ZoneInfo
from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()
class BeehiveViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='testuser', password='12345', timezone='UTC')
        self.test_note = Note.objects.create(user=self.test_user, text='Test note')
        self.test_record = Record.objects.create(user=self.test_user, mood=Mood.objects.filter(id=1).first(), activity=Activity.objects.filter(id=3).first())
        self.test_message = Message.objects.create(user=self.test_user, message='Test message', response='Test response')

    def test_register_view(self):
        response = self.client.post('/register/', {'username': 'testuser2', 'password1': '12345', 'password2': '12345','timezone':'UTC'})
        self.assertEqual(response.status_code, 302)

    def test_mainpage_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/main/')
        self.assertEqual(response.status_code, 200)

    def test_home_view(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_note_creation_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/createnote/', {'text': 'Test note 2'})
        self.assertEqual(response.status_code, 302)

    def test_history_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 200)

    def test_chat_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/chat/', {'message': 'Test message 2'})
        self.assertEqual(response.status_code, 200)

    def test_analytics_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/analytics/', {'start_date': '2022-01-01', 'end_date': '2022-12-31'})
        self.assertEqual(response.status_code, 200)
