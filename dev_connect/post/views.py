from rest_framework import permissions, viewsets, generics
from rest_framework.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import F
from django.shortcuts import get_object_or_404

from .models import Comment, Notification, Post, Clap
from .serializers import (
    CommentSerializer,
    NotificationSerializer,
    PostSerializer,
    ClapSerializer,
)


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

    def save(self, *args, **kwargs):
        post = self.post
        Post.objects.filter(id=post.id).update(comment_count=F('comment_count') + 1)
        Notification.objects.create(
            message=f'user {self.author.username} left '
            f'a new comment on your post {post.title}',
            user=post.author
        )
        super().save(*args, **kwargs)


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
