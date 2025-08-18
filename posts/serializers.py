from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer
from .models import Post, Like, Comment


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'created_at', 'like_count', 'isLiked', 'comment_count')
        read_only_fields = ['created_at']

    def get_serializer_context(self):
        return {'request': self.request}

    def get_like_count(self, obj):
        return obj.like_set.count() or 0

    def get_comment_count(self, obj):
        return obj.comment_set.count()

    def get_isLiked(self, obj):
        request = self.context.get('request', None)
        user = getattr(request, 'user', None)
        print(f"[DEBUG] get_isLiked - user: {user}, authenticated: {user.is_authenticated if user else 'None'}")

        if not user or not user.is_authenticated:
            return False
        return obj.like_set.filter(user=user).exists()


class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user_info = UserSerializer(source='user', read_only=True)
    #user = UserSerializer(read_only=True)
    #post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post')

    class Meta:
        model = Like
        fields = ('id', 'post', 'user_info', 'created_at')
        read_only_fields = ['created_at']

    def get_serializer_context(self):
        return {'request': self.request}

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

