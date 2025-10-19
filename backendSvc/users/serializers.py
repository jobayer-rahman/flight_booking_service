from .models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
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
    access_token_expiration = serializers.IntegerField()
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

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        token_lifetime = api_settings.ACCESS_TOKEN_LIFETIME
        expires_in = int(token_lifetime.total_seconds())

        response_data = {
            'token_type': 'Bearer',
            'refresh_token': str(refresh_token),
            'access_token': str(access_token),
            'access_token_expiration': expires_in,
            'user': user,
        }
        token_response = TokenResponseSerializer(instance=response_data)
        return token_response.data