from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.models import Message  # O'zingizning `Message` modelingizga asoslanadi
from apps.models import Follow
from apps.models import Follow



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
