from django.urls import path
from .views import UserRegistrationAPIView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]

