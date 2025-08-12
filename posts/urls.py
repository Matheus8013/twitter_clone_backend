from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, LikeViewSet, CommentViewSet, FeedView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'likes', LikeViewSet, basename='likes')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('feed/', FeedView.as_view(), name='post-feed'),
    path('', include(router.urls)),
]