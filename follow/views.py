from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Follow
from .serializers import FollowerSerializer, FollowSerializer, FollowingSerializer

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all().order_by('-followed_at')
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    @action(detail=False, methods=['get'])
    def user_following(self, request):
        follows = self.get_queryset().filter(follower=request.user)
        page = self.paginate_queryset(follows)
        if page is not None:
            serializer = FollowingSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = FollowingSerializer(follows, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_followers(self, request):
        follows = self.get_queryset().filter(following=request.user)
        page = self.paginate_queryset(follows)
        if page is not None:
            serializer = FollowerSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = FollowerSerializer(follows, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        follow = self.get_object()
        if follow.follower != request.user:
            return Response({'detail': 'Você não tem permissão para deletar este follow.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
