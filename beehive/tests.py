import pytest
from django.test import Client, TestCase, RequestFactory
from beehive.models import Record, Note, Message, Mood, Activity
from zoneinfo import ZoneInfo
from datetime import datetime
from beehive.views import mainpage
import time
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.models import AnonymousUser
class BeehiveViewsTest(TestCase):

    # Комплект 1 База
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='testuser', password='12345', timezone='UTC')
        self.test_note = Note.objects.create(user=self.test_user, text='Test note')
        self.test_mood = Mood.objects.create(name='Test mood', rate=1)
        self.test_activity = Activity.objects.create(name='Test activity')
        self.test_record = Record.objects.create(user=self.test_user, mood=self.test_mood, activity=self.test_activity)
        self.test_message = Message.objects.create(user=self.test_user, message='Test message', response='Test response')
        self.factory = RequestFactory()



    # тесты на представление mainpage
    def test_mainpage_with_authenticated_user_and_existing_record(self): #аутентифицированный пользователь с существующей записью
        request = self.factory.get('/mainpage')
        request.user = self.test_user
        response = mainpage(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вы уже отмечались сегодня') #Увидит сообщение о том, что отметился

    def test_mainpage_with_authenticated_user_and_no_record(self): #аутентифицированный пользователь без записи
        Record.objects.filter(user=self.test_user).delete()
        request = self.factory.get('/mainpage')
        request.user = self.test_user
        response = mainpage(request)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Вы уже отмечались сегодня') #Не увидит сообщение о том, что отметился, а значит увидит форму

    def test_mainpage_with_anonymous_user(self): #неаутентифицированный пользователь
        request = self.factory.get('/mainpage')
        request.user = AnonymousUser()
        response = mainpage(request)
        self.assertEqual(response.status_code, 302)  #отправится на страницу входа

    def test_mainpage_with_authenticated_user_and_post_request(self): #аутентифицированный пользователь отмечается
        request = self.factory.post('/mainpage', {'form_type': 'record_form', 'mood': self.test_mood.id, 'activity': self.test_activity.id})
        request.user = self.test_user
        response = mainpage(request)
        self.assertEqual(response.status_code, 302)  # После отправки формы должен быть редирект
        self.assertTrue(Record.objects.filter(user=self.test_user).exists())  # Проверяем, что запись создалась

    # тесты на представление history
    def test_history_view_with_authenticated_user_and_existing_records(self): #аутентифицированный пользователь с существующими записями
        self.client.login(username='testuser', password='12345')
        Record.objects.create(user=self.test_user, mood=self.test_mood, activity=self.test_activity)
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'm1')  # Если у пользователя есть записи, то в календаре будет ячейка класса m1

    def test_history_view_with_authenticated_user_and_no_records(self): #аутентифицированный пользователь без записей
        self.client.login(username='testuser', password='12345')
        Record.objects.filter(user=self.test_user).delete()
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'm1')  # Если у пользователя нет записи, то в календаре не будет ячейки класса m1

    def test_history_view_with_anonymous_user(self): #неаутентифицированный пользователь
        request = self.factory.get('/history/')
        request.user = AnonymousUser()
        response = mainpage(request)
        self.assertEqual(response.status_code, 302)  # отправится на страницу входа

    # тесты заметок
    def test_note_creation_view(self): #тест успешного создания заметки
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create_note/', {'text': 'Test note 2'})
        self.assertEqual(response.status_code, 302)

    def test_data_consistency(self): #тест на отображение заметок на странице отметок
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/main/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test note')  # Ожидаем, что заметка будет на странице

    def test_form_validation(self): #тест на валидацию при создании заметки
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create_note/', {'text': ''})  # оставляем поле пустым
        self.assertEqual(response.status_code, 200)  # Форма вернется с ошибкой

    def test_unsuccessful_note_creation(self): #тест на неудачное создание заметки
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create_note/', {'text': ''}) # оставляем поле пустым
        self.assertNotEqual(response.status_code, 302) # Ожидается, что редиректа не будет

    # тесты регистрации и авторизации
    def test_register_view(self): #тест успешной регистрации
        response = self.client.post('/register/', {'username': 'testuser2', 'password1': '1H2e3l4l5o', 'password2': '1H2e3l4l5o','timezone':'UTC'})
        self.assertEqual(response.status_code, 302) # Ожидаем редирект на страницу входа

    def test_unsuccessful_registration(self): #тест на неудачную регистрацию
        response = self.client.post('/register/',{'username': 'testuser3', 'password1': '1H2e3l4l5o', 'password2': '1H2e3l4l5p','timezone': 'UTC'})
        self.assertNotEqual(response.status_code, 302) # Ожидается, что регистрация не пройдет

    def test_unsuccessful_login(self): #тест на неудачную авторизацию
        response = self.client.login(username='wronguser', password='12345')
        self.assertFalse(response) # Ожидается, что авторизация не пройдет

    # глупости
    def test_analytics_view(self): #тест успешного входа на страницу аналитики
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/analytics/', {'start_date': '2022-01-01', 'end_date': '2022-12-31'})
        self.assertEqual(response.status_code, 200)

    def test_chat_form_validation(self): #тест на валидацию формы чата
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/chat/', {'message': ''})  # Пустое сообщение
        self.assertEqual(response.status_code, 200)  # Форма вернется с ошибкой

    def test_LLM_response(self): #Супер тест на получение ответа от ЛЛМ
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/chat/', {'message': 'Hello, world!'})
        self.assertEqual(response.status_code, 200)
        time.sleep(30) # Даем время ЛЛМ на ответ
        new_message = Message.objects.order_by('-id').first()  # Получаем последнее сообщение
        print('new_message.message: ', new_message.message)
        print('new_message.response: ', new_message.response)
        self.assertIsNotNone(new_message.response)  # Проверяем, что ответ не пустой
        self.assertNotEqual(new_message.response, '')  # Проверяем, что ответ ТООООЧНО не пустой