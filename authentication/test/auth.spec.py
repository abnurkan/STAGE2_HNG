from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User, Organisation
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_user_registration(self):
        data = {
            "first_name": "zaza",
            "last_name": "Doe",
            "email": "zaza.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], "success")
        self.assertEqual(response.data['message'], "Registration successful")
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Organisation.objects.count(), 1)

    def test_user_registration_invalid_data(self):
        data = {
            "first_name": "J",
            "last_name": "Doe",
            "email": "invalid-email",
            "password": "pwd",
            "phone": "123"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], "Bad request")
        self.assertEqual(response.data['message'], "Registration unsuccessful")
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
        self.assertEqual(response.data['status'], "success")
        self.assertEqual(response.data['message'], "Login successful")
        self.assertIn('accessToken', response.data['data'])

    def test_user_login_invalid_credentials(self):
        data = {
            "email": "john.doe@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], "Bad request")
        self.assertEqual(response.data['message'], "Authentication failed")

    def test_get_organisation(self):
        user = User.objects.create_user(
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            password="password123",
            phone="1234567890"
        )
        org = Organisation.objects.create(name="John's Organisation")
        org.users.add(user)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
        response = self.client.get(reverse('organisation-detail', args=[org.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "success")
        self.assertEqual(response.data['message'], "Organisation fetched successfully")

    def test_create_organisation(self):
        user = User.objects.create_user(
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            password="password123",
            phone="1234567890"
        )
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
        data = {
            "name": "New Organisation",
            "description": "This is a new organisation"
        }
        response = self.client.post(reverse('organisation-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], "success")
        self.assertEqual(response.data['message'], "Organisation created successfully")

    def test_add_user_to_organisation(self):
        user1 = User.objects.create_user(
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            password="password123",
            phone="1234567890"
        )
        user2 = User.objects.create_user(
            email="jane.doe@example.com",
            first_name="Jane",
            last_name="Doe",
            password="password123",
            phone="0987654321"
        )
        org = Organisation.objects.create(name="John's Organisation")
        org.users.add(user1)
        refresh = RefreshToken.for_user(user1)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
        data = {
            "userId": str(user2.id)
        }
        response = self.client.post(reverse('add-user-to-organisation', args=[org.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "success")
        self.assertEqual(response.data['message'], "User added to organisation successfully")

    def test_get_user_detail(self):
        user1 = User.objects.create_user(
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            password="password123",
            phone="1234567890"
        )
        user2 = User.objects.create_user(
            email="jane.doe@example.com",
            first_name="Jane",
            last_name="Doe",
            password="password123",
            phone="0987654321"
        )
        org = Organisation.objects.create(name="John's Organisation")
        org.users.add(user1)
        refresh = RefreshToken.for_user(user1)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
        response = self.client.get(reverse('user-detail', args=[user1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "success")
        self.assertEqual(response.data['message'], "User fetched successfully")
        response = self.client.get(reverse('user-detail', args=[user2.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
