from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class AdminAuthTests(APITestCase):

    def setUp(self):
        # =========================
        # CREATE USERS
        # =========================
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="admin123"
        )

        self.user = User.objects.create_user(
            username="user",
            email="user@test.com",
            password="user123"
        )

        # =========================
        # URLS (IMPORTANT: NAMESPACE FIXED)
        # =========================
        self.login_url = reverse("accounts:admin-login")
        self.me_url = reverse("accounts:admin-me")
        self.logout_url = reverse("accounts:admin-logout")

    # =========================
    # TEST 1: ADMIN LOGIN SUCCESS
    # =========================
    def test_admin_login_success(self):
        response = self.client.post(self.login_url, {
            "username": "admin",
            "password": "admin123"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tokens", response.data)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])

    # =========================
    # TEST 2: INVALID LOGIN
    # =========================
    def test_invalid_login(self):
        response = self.client.post(self.login_url, {
            "username": "admin",
            "password": "wrongpass"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # =========================
    # TEST 3: NON-SUPERUSER BLOCKED
    # =========================
    def test_non_superuser_login_block(self):
        response = self.client.post(self.login_url, {
            "username": "user",
            "password": "user123"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # =========================
    # TEST 4: ADMIN ME SUCCESS
    # =========================
    def test_admin_me(self):
        refresh = RefreshToken.for_user(self.admin)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "admin")

    # =========================
    # TEST 5: NON-ADMIN ME BLOCKED
    # =========================
    def test_non_admin_me_access(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # =========================
    # TEST 6: LOGOUT SUCCESS
    # =========================
    def test_logout(self):
        refresh = RefreshToken.for_user(self.admin)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.post(self.logout_url, {
            "refresh": str(refresh)
        })

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)