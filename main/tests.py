from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from django.contrib.auth.models import User

PASSWORD = 'Password123'

#pierwszy test kategoria
class CategoryViewSetTest(APITestCase):


    #przed każdym testem zagwarantowany użytkownik
    #podzielone na administratora i zwyklego użytkownika
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password=PASSWORD
        )
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password=PASSWORD
        )
    #testowanie logowania
    def test_login_required(self):
        response = self.client.post(path=reverse('category-list'))
        self.assertEquals(response.status_code, 403)
        self.assertEquals(response.json(),
        #jesli nie zalogowani to brak dostępu do treści
                          {'detail': 'Authentication credentials were not provided.'})
    #tworzenie danych jako zwykly użytkownik
    def test_create_as_user(self):
        self.client.login(username=self.user1.username, password=PASSWORD)
        #tylko administrator może tworzyć kategorie
        response = self.client.post(
            path=reverse('category-list'),
            data={'name': 'Test'}
        )

        self.assertEquals(response.status_code, 403)
        self.assertEquals(response.json(),
            {'detail': 'You do not have permission to perform this action.'}
        )
    #tworzenie danych jako administrator
    def test_create_as_admin(self):
        self.client.login(username=self.admin.username, password=PASSWORD)
        #tworzenie kateogirii
        response = self.client.post(
            path=reverse('category-list'),
            data={'name': 'Test'}
        )
        self.assertEquals(response.json(), {'name': 'Test', 'questions': []})
        self.assertEquals(response.status_code, 201)

#Drugi test, quizy

class QuizViewSetTest(APITestCase):
    #przed każdym testem zagwarantowany użytkownik
    #podzielone na administratora i zwyklego użytkownika
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password=PASSWORD
        )
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password=PASSWORD
        )
    #testowanie logowania
    def test_login_required(self):
        response = self.client.post(path=reverse('quiz-list'))
        self.assertEquals(response.status_code, 403)
        self.assertEquals(response.json(),
                          {
        #jesli nie zalogowani to brak dostępu do treści
                              'detail': 'Authentication credentials were not '
                                        'provided.'})
    #tworzenie danych jako zwykly użytkownik
    def test_create_as_user(self):
        self.client.login(username=self.user1.username, password=PASSWORD)

        response = self.client.post(
            path=reverse('quiz-list'),
            data={'name': 'Test'}
        )

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.json(),
                          {'name': 'Test',
                           'owner': 'user1',
                           'questions': [],
                           'quiz_results': []})
    #tworzenie danych jako administrator
    def test_create_as_admin(self):
        self.client.login(username=self.admin.username, password=PASSWORD)

        response = self.client.post(
            path=reverse('quiz-list'),
            data={'name': 'Test'}
        )
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.json(),
                          {'name': 'Test',
                           'owner': 'admin',
                           'questions': [],
                           'quiz_results': []})

