# authentication/test_authentication.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User, Organisation
from rest_framework_simplejwt.tokens import RefreshToken

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_user_registration(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Organisation.objects.count(), 1)
        user = User.objects.get(email=data['email'])
        organisation = Organisation.objects.get(users=user)
        self.assertEqual(organisation.name, "John's Organisation")

    def test_user_registration_invalid_data(self):
        data = {
            "first_name": "J",
            "last_name": "Doe",
            "email": "invalid-email",
            "password": "pwd",
            "phone": "123"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(User.objects.count(), 0)

    def test_user_login(self):
        user = User.objects.create_user(
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            password="password123",
            phone="1234567890"
        )
        data = {
            "email": "john.doe@example.com",
            "password": "password123"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        data = {
            "email": "john.doe@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class OrganisationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            password="password123",
            phone="1234567890"
        )
        self.organisation = Organisation.objects.create(name="John's Organisation")
        self.organisation.users.add(self.user)
        self.organisation_list_url = reverse('organisations')
        self.token = RefreshToken.for_user(self.user).access_token

    def test_get_organisations_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.organisation_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "John's Organisation")

    def test_get_organisations_unauthenticated(self):
        response = self.client.get(self.organisation_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
