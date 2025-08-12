from rest_framework import viewsets, permissions, status, generics
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

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        try:
            like = Like.objects.get(post_id=pk, user=request.user)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
        following_users_ids = list(following_users_ids) + [user.id]
        return Post.objects.filter(author_id__in=following_users_ids).order_by('-created_at')


class CommentViewSet(viewsets.ModelViewSet):
    # O queryset padrão para a viewset
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        print("--- GET_QUERYSET EXECUTADO ---")
        queryset = super().get_queryset()

        post_id = self.request.query_params.get('post')
        print(f"Valor de 'post' recebido: {post_id}")

        if post_id:
            filtered_queryset = queryset.filter(post_id=post_id)
            print(f"Objetos no queryset filtrado: {filtered_queryset.count()}")
            return filtered_queryset

        print(f"Retornando queryset não filtrado de tamanho: {queryset.count()}")
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

