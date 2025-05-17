from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from apps.models import Profile
from apps.models import Story
from rest_framework import serializers
from apps.models import Follow
from apps.models import Message

from apps.models import Notification, Tag, Post

class StorySerializer(ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'

class NotificationSerializer(ModelSerializer):

class CreateSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = 'is_read', 'created_at', 'post_id', 'notification_type', 'sender'
        model = Story
        fields = '__all__'

class TagsSerializer(ModelSerializer):

class GetUsersSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = 'id','caption', 'file'
        model = User
        fields = '__all__'

class NotificationReadSerializer(ModelSerializer):
    is_read_status = SerializerMethodField()

class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True, min_length=8)

    class Meta:
        model = Notification
        fields = ['is_read', 'is_read_status']
        model = Profile
        fields = ['id', 'user', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'is_private', 'image']


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField()
    following = serializers.StringRelatedField()

    class Meta:
        model = Follow
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = '__all__'

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text', 'file']

    def get_is_read_status(self, obj):
        return "Mardek is read" if obj.is_read else "Notification not read"
