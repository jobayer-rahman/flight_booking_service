from .models import User
from rest_framework import generics
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    UserLogoutSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class UserLoginAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenAPIView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer

class UserLogoutAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Logout successful"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)