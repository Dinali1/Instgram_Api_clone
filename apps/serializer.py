from rest_framework.fields import SerializerMethodField
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


class NotificationReadSerializer(ModelSerializer):
    is_read_status = SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['is_read', 'is_read_status']

    def get_is_read_status(self, obj):
        return "Mardek is read" if obj.is_read else "Notification not read"
