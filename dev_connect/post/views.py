from rest_framework import permissions, viewsets, generics
from rest_framework.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Comment, Notification, Post, Clap
from .serializers import (
    CommentSerializer,
    NotificationSerializer,
    PostSerializer,
    ClapSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return (
            Post.objects.select_related('author')
            .annotate(clap_count=Count('claps'))
            .all()
        )

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
    serializer_class = PostSerializer

    def get_queryset(self):
        return (
            Post.objects.select_related('author')
            .annotate(clap_count=Count('claps'))
            .order_by('-created_at')[:20]
        )

    @method_decorator(cache_page(60 * 5))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class ClapCreateView(generics.CreateAPIView):
    queryset = Clap.objects.all()
    serializer_class = ClapSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if Clap.objects.filter(user=user, post=post).exists():
            raise ValidationError({
                "non_field_errors": ["You've already clapped this post"]
            })

        serializer.save(user=user, post=post)
