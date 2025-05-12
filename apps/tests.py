from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from apps.models import Notification, Post, Tag 

User = get_user_model()

class NotificationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='izzat', password='1')
        self.tag = Tag.objects.create(name='testtag')  # ✅ kerakli tag

        self.post = Post.objects.create(
            caption='Test post',
            file='test.jpg',
            user=self.user,
            tags=self.tag  # ✅ majburiy maydon
        )

        self.notification = Notification.objects.create(
            is_read=True,
            created_at="2024-02-05T00:00:00Z",
            post=self.post,
            notification_type=1,
            sender=self.user,
            user=self.user
        )

    def test_notification_list_view(self):
        url = reverse('get_notification')  # URL nomini `urls.py` bilan tekshiring
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        notification = response.data[0]
        self.assertEqual(notification['sender'], 1)
        self.assertEqual(notification['is_read'], True)
        self.assertEqual(notification['post_id'], self.post.id)
        self.assertEqual(notification['notification_type'], 1)

class TagsListViewTest(APITestCase):
    def test_tags_list_view(self):
        user = User.objects.create_user(username='izzat', password='1')
        tag = Tag.objects.create(name='salom')
        post = Post.objects.create(
            caption='Test post',
            file='/home/izzat/sovga.jpeg',
            user=user,
            tags=tag
        )

        url = reverse('tags-list', kwargs={'tag': 'salom'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['caption'], 'Test post')
        self.assertEqual(response.data[0]['file'], '/home/izzat/sovga.jpeg')

class NotificationCase(APITestCase):
    def test_notification_mark_read_view(self):
        user = User.objects.create_user(username='nima', password='password')
        self.client.force_login(user)
        tag = Tag.objects.create(name='salom')
        post = Post.objects.create(
            caption="Test post",
            file="test.jpg",
            user=user,
            tags=tag
        )
        notification = Notification.objects.create(
            is_read=False,
            created_at="2024-05-01T10:00:00Z",
            post=post,  #
            notification_type=1,
            sender=user,
            user=user
        )
        url = reverse('notification-list', kwargs={'id': notification.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Marked as read')
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
