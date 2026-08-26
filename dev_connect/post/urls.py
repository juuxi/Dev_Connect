from rest_framework.routers import DefaultRouter
from . import views

app_name = 'post'

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'notifications', views.NotificationViewSet, basename='notification')

urlpatterns = router.urls
