from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationAPIView, UserLoginView, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),

    path('', include(router.urls)),
]

