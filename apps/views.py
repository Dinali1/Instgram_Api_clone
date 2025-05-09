from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.models import Notification, Tag, Post
from apps.serializer import NotificationSerializer, TagsSerializer


@extend_schema(tags=['Izzat'])
class NotificationListView(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


@extend_schema(tags=['Izzat'])
class TagsListView(ListAPIView):
    serializer_class = TagsSerializer

    def get_queryset(self):
        tag_name = self.kwargs['tag']
        tag = get_object_or_404(Tag, name=tag_name)
        return Post.objects.filter(tags=tag).order_by('-created_at')


@extend_schema(tags=['Izzat'])
class NotificationMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        notification = get_object_or_404(Notification, id=id, user=request.user)
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return Response({"detail": "Marked as read"})