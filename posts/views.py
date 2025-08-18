from rest_framework import viewsets, permissions, status, generics, request
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from follow.models import Follow

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        author_ids = self.request.query_params.get('author__in')

        if author_ids is not None:
            author_list = author_ids.split(',')
            if author_list and author_list[0]:
                queryset = queryset.filter(author__id__in=author_list)
            else:
                return queryset.none()

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='toggle')
    def toggle_like(self, request):
        post_id = request.data.get('post_id')
        user = request.user
        post = get_object_or_404(Post, pk=post_id)

        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            is_liked = False
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=post)
            is_liked = True

        updated_post_serializer = PostSerializer(post, context={'request': request})
        return Response(updated_post_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def user_likes(self, request):
        likes = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
        following_users_ids = list(following_users_ids) + [user.id]
        return Post.objects.filter(author_id__in=following_users_ids).order_by('-created_at')

    def get_serializer_context(self):
        return {'request': self.request}


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        post_id = self.request.query_params.get('post')

        if post_id:
            filtered_queryset = queryset.filter(post_id=post_id)
            return filtered_queryset

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

