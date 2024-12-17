from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class AuthenticationAPITestCase(APITestCase):
    def setUp(self):
        self.valid_user = {
            "username": "user1@test.com",
            "password": "123456"
        }
        self.invalid_user = {
            "username": "sai@test.com",
            "password": "abcdef"
        }
        User.objects.create_user(
            username=self.valid_user["username"],
            password=self.valid_user["password"]
        )
    def test_login_success(self):
        response = self.client.post("/api/token/", self.valid_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        print("TC001: Đăng nhập thành công")
    def test_login_failure(self):
        response = self.client.post("/api/token/", self.invalid_user)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        print("TC002: Đăng nhập thất bại")

