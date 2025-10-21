from django.urls import path
from .views import (
    RefreshTokenAPIView,
    UserRegisterView,
    UserLoginAPIView,
    UserLogoutAPIView
)


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('refresh-token/', RefreshTokenAPIView.as_view(), name='refresh-token'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
]