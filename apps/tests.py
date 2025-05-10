
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from django.core.files import File
from PIL import Image
import pytest
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Profile,Post,Story,SavedPost,Like,Comment,Follow,Message,PostStat,Tag,Notification

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def test_user2(db):
    return User.objects.create_user(
        username='testuser2',
        email='test2@example.com',
        password='testpass123'
    )

@pytest.fixture
def test_profile(db, test_user):
    return Profile.objects.create(
        user=test_user,
        bio='Test bio',
        website='https://test.com',
        location='Tashkent'
    )

@pytest.fixture
def test_post(db, test_user):
    return Post.objects.create(
        user=test_user,
        caption='Test post',
        file='test.jpg',
        post_type='image'
    )

@pytest.fixture
def test_story(db, test_user):
    return Story.objects.create(
        user=test_user,
        file='story.mp4'
    )

@pytest.fixture
def test_saved_post(db, test_user, test_post):
    return SavedPost.objects.create(
        user=test_user,
        post=test_post
    )

@pytest.fixture
def test_like(db, test_user, test_post):
    return Like.objects.create(
        user=test_user,
        post=test_post
    )

@pytest.fixture
def test_comment(db, test_user, test_post):
    return Comment.objects.create(
        user=test_user,
        post=test_post,
        text='Test comment'
    )

@pytest.fixture
def test_follow(db, test_user, test_user2):
    return Follow.objects.create(
        follower=test_user,
        following=test_user2
    )

@pytest.fixture
def test_message(db, test_user, test_user2):
    return Message.objects.create(
        sender=test_user,
        receiver=test_user2,
        text='Test message'
    )

@pytest.fixture
def test_tag(db):
    return Tag.objects.create(
        name='testtag'
    )

@pytest.fixture
def test_notification(db, test_user, test_user2, test_post):
    return Notification.objects.create(
        user=test_user2,
        sender=test_user,
        notification_type=1,
        post=test_post
    )



@pytest.mark.django_db
class TestProfileModel:
    def test_profile_creation(self, test_profile):
        assert str(test_profile) == "testuser's Profile"
        assert test_profile.bio == 'Test bio'
        assert test_profile.website == 'https://test.com'
        assert test_profile.location == 'Tashkent'
        assert test_profile.is_private is False

    def test_profile_image_resize(self, test_user, tmp_path):
        # Create image and save it to disk
        image_path = tmp_path / "test.jpg"
        img = Image.new('RGB', (500, 500), color='red')
        img.save(image_path)

        # Open image and wrap in Django File object
        with open(image_path, 'rb') as f:
            django_file = File(f)
            django_file.name = "profile_pics/test.jpg"  # Must be a relative safe path
            profile = Profile.objects.create(user=test_user, image=django_file)

        # Verify image was resized
        with Image.open(profile.image.path) as resized_img:
            assert resized_img.size == (300, 300)

@pytest.mark.django_db
class TestPostModel:
    def test_post_creation(self, test_post):
        assert str(test_post) == "testuser's Post - image"
        assert test_post.caption == 'Test post'
        assert test_post.post_type == 'image'
        assert test_post.file.name == 'test.jpg'


    def test_post_types(self):
        assert Post.POST_TYPES == [
            ('image', 'Image Post'),
            ('video', 'Video Post'),
            ('reel', 'Reel'),
        ]


@pytest.mark.django_db
class TestStoryModel:
    def test_story_creation(self, test_story):
        assert str(test_story) == "testuser's Story"
        assert test_story.file.name == 'story.mp4'
        assert test_story.expires_at > timezone.now()

    def test_story_expiration(self):
        user = User.objects.create(username='storyuser')
        story = Story.objects.create(
            user=user,
            file='story2.mp4'
        )
        expected_expiry = timezone.now() + timedelta(hours=24)
        assert abs((story.expires_at - expected_expiry).total_seconds()) < 10

@pytest.mark.django_db
class TestPostViewSet:
    def test_list_posts(self, api_client, test_post):
        url = reverse('post-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['caption'] == 'Test post'


    def test_like_post(self, api_client, test_user, test_post):
        api_client.force_authenticate(user=test_user)
        url = reverse('post-like', kwargs={'pk': test_post.pk})

        # Like the post
        response = api_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        assert Like.objects.count() == 1
        assert Like.objects.first().user == test_user

        # Unlike the post
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Like.objects.count() == 0

    def test_save_post(self, api_client, test_user, test_post):
        api_client.force_authenticate(user=test_user)
        url = reverse('post-save', kwargs={'pk': test_post.pk})

        # Save the post
        response = api_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        assert SavedPost.objects.count() == 1

        # Unsave the post
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert SavedPost.objects.count() == 0

    def test_post_comments(self, api_client, test_post, test_comment):
        url = reverse('post-comments', kwargs={'pk': test_post.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['text'] == 'Test comment'

@pytest.mark.django_db
class TestSignals:
    def test_post_stat_creation(self, test_user):
        post = Post.objects.create(
            user=test_user,
            caption='Signal test',
            file='test.jpg'
        )
        assert hasattr(post, 'stats')
        assert PostStat.objects.filter(post=post).exists()

    def test_like_notification(self, test_user, test_post):
        like = Like.objects.create(
            user=test_user,
            post=test_post
        )
        assert Notification.objects.count() == 1
        notification = Notification.objects.first()
        assert notification.user == test_post.user
        assert notification.sender == test_user
        assert notification.notification_type == 1
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
        response = self.client.patch(self.profile_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_profile_not_found(self):
        response = self.client.patch(reverse('profile-update', kwargs={'username': 'non_existing_user'}), self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
