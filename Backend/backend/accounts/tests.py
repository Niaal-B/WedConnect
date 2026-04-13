from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class AccountsTests(APITestCase):

    def setUp(self):
        # Admin user (allowed)
        self.admin = User.objects.create_superuser(
            username="admin",
            password="admin123",
            email="admin@test.com"
        )

        # Normal user (NOT superuser)
        self.user = User.objects.create_user(
            username="user",
            password="user123",
            email="user@test.com"
        )

        self.login_url = "/api/v1/accounts/login/"
        self.me_url = "/api/v1/accounts/me/"
        self.logout_url = "/api/v1/accounts/logout/"

    # =========================
    # LOGIN TESTS
    # =========================

    def test_admin_login_success(self):
        res = self.client.post(self.login_url, {
            "username": "admin",
            "password": "admin123"
        })

        self.assertEqual(res.status_code, 200)
        self.assertIn("tokens", res.data)
        self.assertIn("access", res.data["tokens"])
        self.assertIn("refresh", res.data["tokens"])

    def test_login_invalid_credentials(self):
        res = self.client.post(self.login_url, {
            "username": "admin",
            "password": "wrongpass"
        })

        self.assertEqual(res.status_code, 400)

    def test_login_non_superuser(self):
        res = self.client.post(self.login_url, {
            "username": "user",
            "password": "user123"
        })

        self.assertEqual(res.status_code, 400)
        self.assertIn("Access denied", str(res.data))

    # =========================
    # ME ENDPOINT
    # =========================

    def test_me_success_admin(self):
        login = self.client.post(self.login_url, {
            "username": "admin",
            "password": "admin123"
        })

        access = login.data["tokens"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        res = self.client.get(self.me_url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["username"], "admin")

    def test_me_without_token(self):
        res = self.client.get(self.me_url)

        # Because DEFAULT permission is IsAuthenticated
        self.assertIn(res.status_code, [401, 403])

    def test_me_non_superuser_forbidden(self):
        refresh = RefreshToken.for_user(self.user)
        access = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        res = self.client.get(self.me_url)

        self.assertEqual(res.status_code, 403)

    # =========================
    # LOGOUT TESTS
    # =========================

    def test_logout_success(self):
        login = self.client.post(self.login_url, {
            "username": "admin",
            "password": "admin123"
        })

        access = login.data["tokens"]["access"]
        refresh = login.data["tokens"]["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        res = self.client.post(self.logout_url, {
            "refresh": refresh
        })

        self.assertEqual(res.status_code, 205)

    def test_logout_without_refresh_token(self):
        login = self.client.post(self.login_url, {
            "username": "admin",
            "password": "admin123"
        })

        access = login.data["tokens"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        res = self.client.post(self.logout_url, {})

        self.assertEqual(res.status_code, 400)
        self.assertIn("Refresh token is required", str(res.data))

    def test_logout_invalid_token(self):
        login = self.client.post(self.login_url, {
            "username": "admin",
            "password": "admin123"
        })

        access = login.data["tokens"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        res = self.client.post(self.logout_url, {
            "refresh": "invalidtoken123"
        })

        self.assertEqual(res.status_code, 400)

    def test_logout_without_auth(self):
        res = self.client.post(self.logout_url, {
            "refresh": "somevalue"
        })

        self.assertIn(res.status_code, [401, 403])