from django.conf import settings
from django.db import models
from django.db.models import F


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    comment_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        post = self.post
        Post.objects.filter(id=post.id).update(comment_count=F('comment_count') + 1)
        Notification.objects.create(
            message=f'user {self.author.username} left '
            f'a new comment on your post {post.title}',
            user=post.author
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Comment on {self.post.title}: {self.content[:20]}'


class Notification(models.Model):
    message = models.CharField(max_length=255, verbose_name='Сообщение')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Адресат',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user}: {self.message[:20]}'


class Clap(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='claps'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='claps'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'],
                name='unique_post_user'
            )
        ]
