from pyexpat.errors import messages

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView

from apps.models import Story
from apps.serializer import StorySerializer, CreateSerializer, GetUsersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from apps.models import Follow
from rest_framework.decorators import api_view
from rest_framework import generics, status
from django.db.models import Q, Max, Count
from apps.models import Message
from apps.serializer import MessageCreateSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Like, SavedPost
from django.contrib.auth.models import User
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
# Create your views here.
from apps.models import Profile
from apps.serializer import RegisterSerializer, ProfileSerializer
from .serializers import CommentSerializer, PostSerializer


@extend_schema(tags=['Shohrux'])
class AllStoriesApiView(ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


@extend_schema(tags=['Shohrux'])
class CreateStoriesApiView(CreateAPIView):
    queryset = Story.objects.all()
    serializer_class = CreateSerializer


@extend_schema(tags=['Shohrux'])
class GetUsersStoriesAPIView(ListAPIView):
    queryset = Story.objects.all()
    serializer_class = GetUsersSerializer


@extend_schema(tags=['Shohrux'])
class ViewsUserAPIView(CreateAPIView):
    queryset = Story.objects.all()
    serializer_class = CreateSerializer




class FollowUnfollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user == target_user:
            return Response({"detail": "Cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.get_or_create(follower=request.user, following=target_user)
        return Response({"detail": "Followed"})

    def delete(self, request, username):
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        Follow.objects.filter(follower=request.user, following=target_user).delete()
        return Response({"detail": "Unfollowed"})

@api_view(['GET'])
def followers_list(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    followers = user.followers.all().values_list('follower__username', flat=True)
    return Response(list(followers))

@api_view(['GET'])
def following_list(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    following = user.following.all().values_list('following__username', flat=True)
    return Response(list(following))



class MessageListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            other_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        messages = Message.objects.filter(
            Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user)
        ).order_by('created_at')

        # Belgilash: o'qilmagan xabarlarni is_read=True ga o'zgartiramiz
        Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        try:
            receiver = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, receiver=receiver)
            return Response(MessageSerializer(serializer.instance).data, status=201)
        return Response(serializer.errors, status=400)

class ChatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # O'zaro xabar almashgan foydalanuvchilar
        contacts = Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).values('sender', 'receiver')

        usernames = set()
        for c in contacts:
            if c['sender'] != user.id:
                usernames.add(c['sender'])
            if c['receiver'] != user.id:
                usernames.add(c['receiver'])

        result = []
        for uid in usernames:
            contact = User.objects.get(id=uid)
            last_msg = Message.objects.filter(
                Q(sender=user, receiver=contact) | Q(sender=contact, receiver=user)
            ).order_by('-created_at').first()

            unread_count = Message.objects.filter(
                sender=contact,
                receiver=user,
                is_read=False
            ).count()

            result.append({
                "username": contact.username,
                "last_message": last_msg.text if last_msg else "",
                "unread_count": unread_count
            })

        return Response(result)




@extend_schema(tags=['Fazliddin Register api', ])
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_201_CREATED)

@extend_schema(tags=['Fazliddin Profile  api', ])
class ProfileView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'

    def get_object(self):
        return User.objects.get(username=self.kwargs['username'])


@extend_schema(tags=['Fazliddin Update  api', ])
class ProfileUpdateView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user'

    def get_object(self):
        return User.objects.get(username=self.kwargs['username'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


@extend_schema(tags=['Posts'])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'post_type', 'location', 'tags__name']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post', 'delete'])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if request.method == 'POST':
            if created:
                    return Response({'detail': 'Liked'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Already liked'}, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            like.delete()
            return Response({'detail': 'Unliked'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    @action(detail=True, methods=['post', 'delete'])
    def save(self, request, pk=None):
        post = self.get_object()
        saved, created = SavedPost.objects.get_or_create(user=request.user, post=post)
        if request.method == 'POST':
            if created:
                return Response({'detail': 'Saved'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Already saved'}, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            saved.delete()
            return Response({'detail': 'Unsaved'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        post = self.get_object()
        if request.method == 'GET':
            comments = post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Not allowed'}, status=status.HTTP_404_NOT_FOUND)

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
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
class NotificationViewSet(APIView):

    def get(self, request, id):
        notification = get_object_or_404(Notification, pk=id)
        if notification.is_read:
            return Response({"detail": "Marked as read"})
        else:
            return Response({"detail": "Notification not read"})
