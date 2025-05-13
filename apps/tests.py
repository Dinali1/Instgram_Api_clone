from django.test import TestCase

# Create your tests here.

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

class RegisterAPITestCase(APITestCase):

    def setUp(self):
        self.register_url = reverse('api-register')
        self.user_data = {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "strongpassword123"
        }

    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertTrue(User.objects.filter(username="john_doe").exists())

class ProfileAPITestCase(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "alifayz",
            "email": "aliddinfayz@gmail.com",
            "password": "something123"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.profile_url = reverse('profile-detail', kwargs={'username': 'john_doe'})

    def test_profile_retrieve_success(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_profile_not_found(self):
        response = self.client.get(reverse('profile-detail', kwargs={'username': 'non_existing_user'}))
        self.assertEqual(response.status_code, 'Not Found')

class ProfileUpdateAPITestCase(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "strongpassword123"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.profile_url = reverse('profile-update', kwargs={'username': 'john_doe'})
        self.update_data = {
            "bio": "Updated bio",
            "location": "Samarkand"
        }

    def test_update_profile_success(self):
        response = self.client.patch(self.profile_url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], self.update_data['bio'])
        self.assertEqual(response.data['location'], self.update_data['location'])

    def test_update_profile_invalid_field(self):
        invalid_data = {
            "bio": "New bio",
            "location": "InvalidLocation12345678901234567890123456789012345"  # 100+ characters
        }

    def test_profile_fields(self):
        response = self.client.get(reverse('api_stories'), self.data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_profile_not_found(self):
        response = self.client.patch(reverse('profile-update', kwargs={'username': 'non_existing_user'}), self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
