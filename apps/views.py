from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView

from apps.models import Story
from apps.serializer import StorySerializer, CreateSerializer, GetUsersSerializer


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
from django.contrib.auth.models import User
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
# Create your views here.

from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Like, SavedPost

from apps.models import Profile
from apps.serializer import RegisterSerializer, ProfileSerializer
from .serializers import CommentSerializer, PostSerializer


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

