from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Post, Like, Comment


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'content', 'author_username', 'created_at', 'like_count', 'comment_count')
        read_only_fields = ['created_at']

    def get_like_count(self, obj):
        return obj.like_set.count()

    def get_comment_count(self, obj):
        return obj.comment_set.count()

class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user_info = UserSerializer(source='user', read_only=True)
    #user = UserSerializer(read_only=True)
    #post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post')

    class Meta:
        model = Like
        fields = ('id', 'post', 'user_info', 'created_at')
        read_only_fields = ['created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        post = validated_data['post']

        return Like.objects.create(user=user, post=post)

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content', 'created_at')
        read_only_fields = ['author', 'created_at']

