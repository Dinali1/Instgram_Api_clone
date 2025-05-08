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

from apps.models import Profile
from apps.serializer import RegisterSerializer, ProfileSerializer


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

