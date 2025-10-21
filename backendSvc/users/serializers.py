from .models import User
from .utils import get_token
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.settings import api_settings


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'msisdn',
            'role',
            'password',
            'confirm_password'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"detail": "Password do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'is_banned']

class TokenResponseSerializer(serializers.Serializer):
    token_type = serializers.CharField()
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()
    expiration = serializers.IntegerField()

class LoginResponseSerializer(serializers.Serializer):
    token = TokenResponseSerializer()
    user = UserInfoSerializer()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        if user.is_banned:
            raise serializers.ValidationError("User is banned.")

        token = get_token(user=user)
        response_data = {
            'token': token,
            'user': user,
        }
        token_response = LoginResponseSerializer(instance=response_data)
        return token_response.data

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs["refresh_token"]
        token = get_token(refresh_token_str=refresh_token)
        token_data = TokenResponseSerializer(instance=token)
        return token_data.data

class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh_token"]
        try:
            self.refresh_token = RefreshToken(self.token)
        except TokenError:
            raise serializers.ValidationError("Invalid or expired token.")
        return attrs

    def save(self, **kwargs):
        self.refresh_token.blacklist()