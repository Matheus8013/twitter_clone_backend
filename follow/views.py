

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Follow
from .serializer import FollowerSerializer

# Create your views here.

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = (permissions.IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    @action(detail=False, methods=['get'])
    def user_following(self, request):
        follows = Follow.objects.filter(follower=request.user)
        serializer = self.get_serializer(follows, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_followers(self, request):
        follows = Follow.objects.filter(following=request.user)
        serializer = self.get_serializer(follows, many=True)
        return Response(serializer.data)
