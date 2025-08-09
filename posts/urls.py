from django.urls import path
from .views import PostView, FeedView

urlpatterns = [
    path('posts/create/', PostView.as_view(), name='create-post'),
    path('feed/' , FeedView.as_view(), name='feed'),
]