import pytest
from django.test import Client, TestCase
from beehive.models import Record, Note, Message, Mood, Activity
from zoneinfo import ZoneInfo
from datetime import datetime
import time
from django.contrib.auth import get_user_model
User = get_user_model()
class BeehiveViewsTest(TestCase):

    # Комплект 1 База
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='testuser', password='12345', timezone='UTC')
        self.test_note = Note.objects.create(user=self.test_user, text='Test note')
        self.test_record = Record.objects.create(user=self.test_user, mood=Mood.objects.filter(id=1).first(), activity=Activity.objects.filter(id=3).first())
        self.test_message = Message.objects.create(user=self.test_user, message='Test message', response='Test response')

    def test_register_view(self): #тест успешной регистрации
        response = self.client.post('/register/', {'username': 'testuser2', 'password1': '1H2e3l4l5o', 'password2': '1H2e3l4l5o','timezone':'UTC'})
        self.assertEqual(response.status_code, 302)

    def test_mainpage_view(self): #тест успешного входа на страницу c отметками
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/main/')
        self.assertEqual(response.status_code, 200)

    def test_home_view(self): #тест успешного входа на главную страницу
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_note_creation_view(self): #тест успешного создания заметки
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create_note/', {'text': 'Test note 2'})
        self.assertEqual(response.status_code, 302)

    def test_history_view(self): #тест успешного входа на страницу истории
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 200)

    def test_chat_view(self): #тест успешной отправки сообщения
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/chat/', {'message': 'Test message 2'})
        self.assertEqual(response.status_code, 200)

    def test_analytics_view(self): #тест успешного входа на страницу аналитики
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/analytics/', {'start_date': '2022-01-01', 'end_date': '2022-12-31'})
        self.assertEqual(response.status_code, 200)
#Комплект 2 провалы и просто штуки

    def test_authenticated_access(self): #тест на доступ к страницам без авторизации
        self.client.logout()
        response = self.client.get('/main/')
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект на страницу входа

    def test_data_consistency(self): #тест на отображение заметок на странице
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/main/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test note')  # Ожидаем, что заметка будет на странице

    def test_form_validation(self): #тест на валидацию при создании заметки
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create_note/', {'text': ''})  # оставляем поле пустым
        self.assertEqual(response.status_code, 200)  # Форма вернется с ошибкой

    def test_correct_redirection(self): #тест на корректное перенаправление
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create_note/', {'text': 'Test note 2'}, follow=True)
        self.assertEqual(response.redirect_chain[0][0], '/main/')  # Ожидаем перенаправление на главную страницу
#    Комплект 3 Неудачи

    def test_unsuccessful_registration(self): #тест на неудачную регистрацию
        response = self.client.post('/register/',
                                    {'username': 'testuser3', 'password1': '1H2e3l4l5o', 'password2': '1H2e3l4l5p',
                                     'timezone': 'UTC'})
        self.assertNotEqual(response.status_code, 302) # Ожидается, что регистрация не пройдет

    def test_unsuccessful_login(self): #тест на неудачную авторизацию
        response = self.client.login(username='wronguser', password='12345')
        self.assertFalse(response) # Ожидается, что авторизация не пройдет

    def test_unsuccessful_note_creation(self): #тест на неудачное создание заметки
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create_note/', {'text': ''}) # Федор Двинятин, откройте черный ящик, там пусто!
        self.assertNotEqual(response.status_code, 302)

    def test_chat_form_validation(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/chat/', {'message': ''})  # Пустое сообщение
        self.assertEqual(response.status_code, 200)  # Форма вернется с ошибкой

    def test_post_request(self): #Супер тест на получение ответа от ЛЛМ
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/chat/', {'message': 'Hello, world!'})
        self.assertEqual(response.status_code, 200)
        time.sleep(30) # Даем время ЛЛМ на ответ
        new_message = Message.objects.order_by('-id').first()  # Получаем последнее сообщение
        print('new_message.message: ', new_message.message)
        print('new_message.response: ', new_message.response)
        self.assertIsNotNone(new_message.response)  # Проверяем, что ответ не пустой
        self.assertNotEqual(new_message.response, '')  # Проверяем, что ответ ТООООЧНО не пустой