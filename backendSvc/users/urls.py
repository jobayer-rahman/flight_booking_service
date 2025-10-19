from django.urls import path
from .views import UserRegisterView, LoginAPIView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name="login"),
]