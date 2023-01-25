from django.contrib.auth import get_user_model
from django.test import tag
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from auth_app.serializers import error_messages

User = get_user_model()


@tag('auth')
class AuthApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        data = {
            'email': 'rahmatovolim3@gmail.com',
            'password': make_password('tester25')
        }
        cls.user = User.objects.create(**data, is_active=True)

    def test_sign_in(self):
        sign_in = reverse_lazy('auth_app:sign-in')

        data = {
            'email': self.user.email,
            'password': 'wrong_password',
        }
        response = self.client.post(sign_in, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        data['password'] = 'tester25'
        response = self.client.post(sign_in, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        data['email'] = 'test@mail.com'
        response = self.client.post(sign_in, data, format='json')
        self.assertEqual(response.json(), {"email": [error_messages['wrong_credentials']]})
        data['email'] = self.user.email
        response = self.client.post(sign_in, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_sign_up(self):
        url = reverse_lazy('auth_app:sign-up')
        data = {
          "first_name": "olim",
          "last_name": "rakhmatov",
          "email": "olim@gmail.com",
          "password1": "qweasdzxc98",
          "password2": "qweasdzxc99"
        }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        data["password2"] = 'qweasdzxc98'
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        data["email"] = 'wrong.com'
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        data["email"] = 'olim@gmail.com'
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.json(), {'email': [error_messages['already_registered']]})
