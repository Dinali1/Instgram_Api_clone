from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Like, SavedPost
from .serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend

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


