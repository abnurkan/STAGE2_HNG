# authentication/test_authentication.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User, Organisation
from rest_framework_simplejwt.tokens import RefreshToken


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
