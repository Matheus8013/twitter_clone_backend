from rest_framework import serializers

from follow.models import Follow
from users.models import User
from users.serializers import UserSerializer


class FollowingSerializer(serializers.ModelSerializer):
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('id', 'following')

class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('id', 'follower')

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.PrimaryKeyRelatedField(read_only=True)
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following')