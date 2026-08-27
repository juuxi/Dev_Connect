from rest_framework import permissions, viewsets, generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Comment, Notification, Post
from .serializers import CommentSerializer, NotificationSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('post', 'author')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().select_related('user')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ListMainFeed(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')[:20]
    serializer_class = PostSerializer

    @method_decorator(cache_page(60 * 5))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)
