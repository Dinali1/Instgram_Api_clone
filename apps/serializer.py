from rest_framework.serializers import ModelSerializer

from apps.models import Notification, Tag, Post


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = 'is_read', 'created_at', 'post_id', 'notification_type', 'sender'


class TagsSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = 'caption', 'file'










































