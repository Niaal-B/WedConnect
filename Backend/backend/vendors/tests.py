from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Category, State, District, Vendor


# =========================
# BASE SETUP
# =========================
class BaseAPITest(APITestCase):

    def setUp(self):

        # ADMIN USER
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="admin123"
        )

        # NORMAL USER
        self.user = User.objects.create_user(
            username="user@test.com",
            email="user@test.com",
            password="user123"
        )

        # CATEGORY
        self.category = Category.objects.create(name="Photography")

        # STATE + DISTRICT
        self.state = State.objects.create(name="Kerala")
        self.district = District.objects.create(
            name="kannur",
            state=self.state
        )

        # AUTH TOKEN CLIENT HELPERS
        self.client.login(username="admin@test.com", password="admin123")


# =========================
# CATEGORY TESTS
# =========================
class CategoryTests(BaseAPITest):

    def test_create_category_admin_only(self):
        self.client.force_authenticate(user=self.admin)

        url = "/api/v1/vendors/categories/"
        data = {"name": "Catering"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_create_category_forbidden_for_normal_user(self):
        self.client.force_authenticate(user=self.user)

        url = "/api/v1/vendors/categories/"
        data = {"name": "Catering"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# =========================
# STATE & DISTRICT TESTS
# =========================
class LocationTests(BaseAPITest):

    def test_get_states(self):
        url = "/api/v1/vendors/states/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_district_by_state(self):
        url = f"/api/v1/vendors/districts/?state={self.state.name}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], "kannur")


# =========================
# VENDOR TESTS
# =========================
class VendorTests(BaseAPITest):

    def test_create_vendor_admin_only(self):
        self.client.force_authenticate(user=self.admin)

        url = "/api/v1/vendors/vendors/create/"

        data = {
            "name": "John Studio",
            "email": "john@test.com",
            "contact_number": "123456789",
            "whatsapp_number": "123456789",
            "years_of_experience": 5,
            "category": self.category.id,
            "districts": [self.district.id],
            "joining_date": "2024-01-01"
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)

    def test_vendor_login_success(self):
        user = User.objects.create_user(
            username="vendor@test.com",
            email="vendor@test.com",
            password="vendor123"
        )

        vendor = Vendor.objects.create(
            user=user,
            name="Vendor Test",
            email="vendor@test.com",
            contact_number="111111111",
            whatsapp_number="111111111",
            years_of_experience=2,
            category=self.category,
            joining_date="2024-01-01"
        )

        url = "/api/v1/vendors/vendors/login/"

        response = self.client.post(url, {
            "email": "vendor@test.com",
            "password": "vendor123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_vendor_login_invalid(self):
        url = "/api/v1/vendors/vendors/login/"

        response = self.client.post(url, {
            "email": "wrong@test.com",
            "password": "wrong"
        })

        self.assertEqual(response.status_code, 401)


# =========================
# ACTIVATE / DEACTIVATE
# =========================
class VendorStatusTests(BaseAPITest):

    def setUp(self):
        super().setUp()

        user = User.objects.create_user(
            username="vendor@test.com",
            email="vendor@test.com",
            password="vendor123"
        )

        self.vendor = Vendor.objects.create(
            user=user,
            name="Vendor",
            email="vendor@test.com",
            contact_number="999999999",
            whatsapp_number="999999999",
            years_of_experience=3,
            category=self.category,
            joining_date="2024-01-01"
        )

    def test_deactivate_vendor(self):
        self.client.force_authenticate(user=self.admin)

        url = f"/api/v1/vendors/vendors/{self.vendor.id}/deactivate/"
        response = self.client.patch(url)

        self.vendor.refresh_from_db()
        self.assertFalse(self.vendor.is_active)

    def test_activate_vendor(self):
        self.vendor.is_active = False
        self.vendor.save()

        self.client.force_authenticate(user=self.admin)

        url = f"/api/v1/vendors/vendors/{self.vendor.id}/activate/"
        response = self.client.patch(url)

        self.vendor.refresh_from_db()
        self.assertTrue(self.vendor.is_active)