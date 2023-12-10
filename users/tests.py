from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from .models import User


# Create your tests here.
class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.path = reverse('register')

    def test_register_user_get(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_user_post(self):
        data = {
            'name': 'vlad',
            'last_name': 'lyahovich',
            'username': 'vlad',
            'email': 'belouskovlad@gmail.com',
            'password1': 'admin12345',
            'password2': 'admin12345',
        }
        response = self.client.post(self.path, data)
        username = data['username']

        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username=username).exists())

