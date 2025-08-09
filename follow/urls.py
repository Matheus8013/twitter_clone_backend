from django.urls import path
from .views import FollowViewSet

follow_list = FollowViewSet.as_view({'get': 'list'})
follow_create = FollowViewSet.as_view({'post': 'create'})
my_following = FollowViewSet.as_view({'get': 'my_following'})
my_followers = FollowViewSet.as_view({'get': 'my_followers'})

urlpatterns = [
    path('', follow_list, name='follow-list'),
    path('create/', follow_create, name='follow-create'),
    path('my-following/', my_following, name='my-following'),
    path('my-followers/', my_followers, name='my-followers'),
]

