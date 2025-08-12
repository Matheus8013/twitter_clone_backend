from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Follow
from .serializers import FollowerSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all().order_by('-followed_at')
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    @action(detail=False, methods=['get'])
    def user_following(self, request):
        follows = Follow.objects.filter(follower=request.user).order_by('-followed_at')
        page = self.paginate_queryset(follows)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(follows, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_followers(self, request):
        follows = Follow.objects.filter(following=request.user).order_by('-followed_at')
        page = self.paginate_queryset(follows)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(follows, many=True)
        return Response(serializer.data)
