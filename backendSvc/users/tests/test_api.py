from users.models import User
from django.urls import reverse
from users.factories import UserFactory
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

class BaseUserAPITestCase(APITestCase):
    """Common setup for all API tests."""
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.refresh_token_url = reverse('refresh-token')
        self.logout_url = reverse('logout')
        self.password = "testPassword123"
        self.user = UserFactory(password=self.password)

class UserRegisterAPITests(BaseUserAPITestCase):
    def test_register_user_success(self):
        payload = {
            "username": "newuser",
            "first_name": "john",
            "last_name": "doe",
            "email": "john@gmail.com",
            "msisdn": "01738553240",
            "role": "customer",
            "password": "password123",
            "confirm_password": "password123"
        }
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_user_with_wrong_password(self):
        payload = {
            "username": "newuser",
            "first_name": "john",
            "last_name": "doe",
            "email": "john@gmail.com",
            "msisdn": "01738553240",
            "role": "customer",
            "password": "password123",
            "confirm_password": "wrongpassword123"
        }
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Password do not match.", str(response.data))

class UserLoginAPITests(BaseUserAPITestCase):
    def test_login_success(self):
        payload = {
            "username": self.user.username,
            "password": self.password
        }
        response = self.client.post(self.login_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("access_token", response.data["token"])
        self.assertIn("refresh_token", response.data["token"])

    def test_login_with_invalid_credentials(self):
        payload = {
            "username": self.user.username,
            "password": "wrong_password"
        }
        response = self.client.post(self.login_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid username or password.", str(response.data))

    def test_login_for_banned_user(self):
        self.user.is_banned = True
        self.user.save()
        
        payload = {
            "username": self.user.username,
            "password": self.password
        }
        response = self.client.post(self.login_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("User is banned.", str(response.data))


class RefreshTokenAPITests(BaseUserAPITestCase):
    def test_refresh_token_success(self):
        refresh_token = RefreshToken.for_user(self.user)
        payload = {
            "refresh_token": str(refresh_token),
        }
        response = self.client.post(self.refresh_token_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_refresh_token_invalid(self):
        payload = {
            "refresh_token": "invalid_refreesh_token",
        }
        response = self.client.post(self.refresh_token_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserLogoutAPITests(BaseUserAPITestCase):
    def test_logout_success(self):
        refresh_token = RefreshToken.for_user(self.user)
        payload = {
            "refresh_token": str(refresh_token),
        }
        response = self.client.post(self.logout_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Logout successful")

    def test_logout_with_invalid_refresh_token(self):
        payload = {
            "refresh_token": "invalid_refreesh_token",
        }
        response = self.client.post(self.logout_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid or expired token.", response.data["detail"])