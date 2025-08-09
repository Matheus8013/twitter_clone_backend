from rest_framework import serializers

from follow.models import Follow


class FollowerSerializer(serializers.ModelSerializer):
    follower_username = serializers.ReadOnlyField(source='follower.username')
    following_username = serializers.ReadOnlyField(source='follower.username')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'follower_username', 'following', 'following_username', 'followed_at']
        read_only_fields = [ 'follower' ,'followed_at']