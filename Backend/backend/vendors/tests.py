from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Category, State, District, Vendor


class VendorAPITests(APITestCase):

    def setUp(self):

        # =========================
        # CREATE ADMIN USER
        # =========================
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="admin123"
        )

        # =========================
        # AUTH
        # =========================
        self.client.force_authenticate(user=self.admin)

        # =========================
        # BASE DATA
        # =========================
        self.category = Category.objects.create(name="Photography")

        self.state = State.objects.create(name="Kerala")

        self.district = District.objects.create(
            name="Kochi",
            state=self.state
        )

    # =========================
    # CATEGORY TEST
    # =========================
    def test_create_category(self):
        url = "/api/v1/vendors/categories/"

        data = {
            "name": "Music"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    # =========================
    # STATE LIST TEST
    # =========================
    def test_list_states(self):
        url = "/api/v1/vendors/states/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # =========================
    # DISTRICT FILTER TEST
    # =========================
    def test_district_filter_by_state(self):
        url = "/api/v1/vendors/districts/?state=Kerala"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Kochi")

    # =========================
    # VENDOR CREATE TEST
    # =========================
    def test_create_vendor(self):
        url = "/api/v1/vendors/vendors/create/"

        data = {
            "name": "John Studio",
            "email": "john@example.com",
            "contact_number": "9876543210",
            "whatsapp_number": "9876543210",
            "years_of_experience": 5,
            "category": self.category.id,
            "districts": [self.district.id],
            "joining_date": "2024-01-01"
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)

        vendor = Vendor.objects.first()

        # check auto user created
        self.assertTrue(User.objects.filter(username="john@example.com").exists())

    # =========================
    # VENDOR LIST TEST
    # =========================
    def test_vendor_list(self):
        Vendor.objects.create(
            user=self.admin,
            name="Test Vendor",
            email="test@vendor.com",
            contact_number="12345678",
            whatsapp_number="12345678",
            years_of_experience=2,
            category=self.category,
            joining_date="2024-01-01"
        )

        url = "/api/v1/vendors/vendors/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # =========================
    # VENDOR DEACTIVATE TEST
    # =========================
    def test_vendor_deactivate(self):

        vendor_user = User.objects.create_user(
            username="vendor@test.com",
            email="vendor@test.com",
            password="123"
        )

        vendor = Vendor.objects.create(
            user=vendor_user,
            name="Test Vendor",
            email="vendor@test.com",
            contact_number="12345678",
            whatsapp_number="12345678",
            years_of_experience=2,
            category=self.category,
            joining_date="2024-01-01"
        )

        url = f"/api/v1/vendors/vendors/{vendor.id}/deactivate/"

        response = self.client.patch(url)

        vendor.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(vendor.is_active)

    # =========================
    # VENDOR ACTIVATE TEST
    # =========================
    def test_vendor_activate(self):

        vendor_user = User.objects.create_user(
            username="vendor2@test.com",
            email="vendor2@test.com",
            password="123"
        )

        vendor = Vendor.objects.create(
            user=vendor_user,
            name="Test Vendor 2",
            email="vendor2@test.com",
            contact_number="12345678",
            whatsapp_number="12345678",
            years_of_experience=2,
            category=self.category,
            joining_date="2024-01-01",
            is_active=False
        )

        url = f"/api/v1/vendors/vendors/{vendor.id}/activate/"

        response = self.client.patch(url)

        vendor.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(vendor.is_active)