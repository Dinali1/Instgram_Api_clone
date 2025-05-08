from django.contrib.auth.models import User
from rest_framework.fields import CharField

from rest_framework.serializers import ModelSerializer

from apps.models import Profile


class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True, min_length=8)

    class Meta:
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


