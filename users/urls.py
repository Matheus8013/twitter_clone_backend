from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationAPIView, UserLoginView, UserViewSet, CurrentUserView, PasswordChangeView, \
    UserProfileView

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('auth/user/', CurrentUserView.as_view(), name='current-user'),
    path('auth/password/change/', PasswordChangeView.as_view(), name='password-change'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    path('', include(router.urls)),
]

