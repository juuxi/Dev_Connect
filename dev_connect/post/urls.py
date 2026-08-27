from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'post'

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'notifications', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('posts/main_feed/', views.ListMainFeed.as_view()),
    path('', include(router.urls)),
]
