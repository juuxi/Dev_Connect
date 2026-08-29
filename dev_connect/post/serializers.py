from rest_framework import serializers
from .models import Comment, Notification, Post, Clap


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'author',
            'claps',
            'comment_count',
            'created_at',
        ]
        read_only_fields = ['author', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'user', 'created_at']
        read_only_fields = ['created_at']


class ClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clap
        fields = ['id', 'post', 'user']
        read_only_fields = ['post', 'user']
