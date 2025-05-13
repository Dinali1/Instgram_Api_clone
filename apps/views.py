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
