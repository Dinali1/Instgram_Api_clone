from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.models import Message  # O'zingizning `Message` modelingizga asoslanadi
from apps.models import Follow
from apps.models import Follow
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User



class MessageListApiTestCase(APITestCase):
    def setUp(self):
        # Foydalanuvchilarni yaratish
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123',
            email='user1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123',
            email='user2@example.com'
        )

        # Xabarlar yaratish
        Message.objects.create(sender=self.user1, receiver=self.user2, text="Hello from user1")
        Message.objects.create(sender=self.user2, receiver=self.user1, text="Hi user1, it's user2")
        Message.objects.create(sender=self.user1, receiver=self.user2, text="How are you?")

    def test_get_message_list_by_username(self):
        # Xabarlar ro'yxatini olish
        url = reverse('message_list_create', args=[self.user2.username])  # Xabarlar uchun URL
        self.client.force_authenticate(user=self.user1)  # Foydalanuvchini avtorizatsiya qilish
        response = self.client.get(url)  # GET so'rovini yuborish
        self.assertEqual(response.status_code, 200)  # Status kodi 200 bo'lishi kerak
        self.assertEqual(len(response.data), 3)  # 3 ta xabar mavjud

    def test_send_message(self):
        # Yangi xabar yuborish
        url = reverse('message_list_create', args=[self.user2.username])
        data = {'text': 'Test message from user1'}
        self.client.force_authenticate(user=self.user1)  # Foydalanuvchini avtorizatsiya qilish
        response = self.client.post(url, data, format='json')  # POST so'rovini yuborish
        self.assertEqual(response.status_code, 201)  # Yaratish muvaffaqiyatli bo'lsa, 201 qaytishi kerak
        self.assertEqual(response.data['text'], 'Test message from user1')  # Yuborilgan xabar matni

    def test_chat_list_view(self):
        # Chatlar ro'yxatini olish
        url = reverse('chat_list')
        self.client.force_authenticate(user=self.user1)  # Foydalanuvchini avtorizatsiya qilish
        response = self.client.get(url)  # GET so'rovini yuborish
        self.assertEqual(response.status_code, 200)  # Status kodi 200 bo'lishi kerak
        self.assertEqual(len(response.data), 1)  # Bitta chat (user2) ro'yxatda bo'lishi kerak
        self.assertEqual(response.data[0]['username'], 'user2')  # Chatda user2 bo'lishi kerak



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
