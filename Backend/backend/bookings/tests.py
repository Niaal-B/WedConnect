from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from datetime import date, timedelta

from vendors.models import Vendor, Category, State, District
from bookings.models import Booking, Payment


class BookingAPITest(APITestCase):

    def setUp(self):

        # =========================
        # AUTH SETUP (PRODUCTION WAY)
        # =========================
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="vendor@test.com",
            email="vendor@test.com",
            password="password123"
        )

        self.client.force_authenticate(user=self.user)

        # =========================
        # MASTER DATA
        # =========================
        self.category = Category.objects.create(name="Photography")
        self.state = State.objects.create(name="Test State")
        self.district = District.objects.create(
            name="Test District",
            state=self.state
        )

        # =========================
        # VENDOR PROFILE
        # =========================
        self.vendor = Vendor.objects.create(
            user=self.user,
            name="Vendor Test",
            email="vendor@test.com",
            contact_number="1234567890",
            whatsapp_number="1234567890",
            years_of_experience=5,
            category=self.category,
            joining_date=date.today()
        )
        self.vendor.districts.add(self.district)

        # =========================
        # URLS (SOURCE OF TRUTH)
        # =========================
        self.create_url = reverse("booking-create")
        self.list_url = reverse("vendor-bookings")

        self.add_payment_url = lambda pk: reverse("booking-add-payment", args=[pk])
        self.update_url = lambda pk: reverse("booking-update", args=[pk])
        self.delete_url = lambda pk: reverse("booking-delete", args=[pk])

    # =========================
    # CREATE BOOKING
    # =========================
    def test_create_booking_success(self):

        payload = {
            "customer_name": "John",
            "district": self.district.id,
            "address": "Test Address",
            "phone_number": "1234567890",
            "total_amount": "1000.00",
            "advance_amount": "200.00",
            "dates": [
                {
                    "event_date": str(date.today() + timedelta(days=1)),
                    "slots": [
                        {"start_time": "10:00:00", "end_time": "12:00:00"}
                    ]
                }
            ]
        }

        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 1)

    # =========================
    # INVALID PHONE
    # =========================
    def test_invalid_phone_number(self):

        payload = {
            "customer_name": "John",
            "district": self.district.id,
            "address": "Test Address",
            "phone_number": "123",  # invalid
            "total_amount": "1000.00",
            "advance_amount": "200.00",
            "dates": []
        }

        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # =========================
    # ADVANCE > TOTAL
    # =========================
    def test_advance_exceeds_total(self):

        payload = {
            "customer_name": "John",
            "district": self.district.id,
            "address": "Test",
            "phone_number": "1234567890",
            "total_amount": "1000.00",
            "advance_amount": "2000.00",
            "dates": []
        }

        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # =========================
    # INVALID SLOT TIME
    # =========================
    def test_invalid_slot_time(self):

        payload = {
            "customer_name": "John",
            "district": self.district.id,
            "address": "Test",
            "phone_number": "1234567890",
            "total_amount": "1000.00",
            "advance_amount": "200.00",
            "dates": [
                {
                    "event_date": str(date.today() + timedelta(days=1)),
                    "slots": [
                        {"start_time": "12:00:00", "end_time": "10:00:00"}
                    ]
                }
            ]
        }

        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # =========================
    # ADD PAYMENT SUCCESS
    # =========================
    def test_add_payment_success(self):

        booking = Booking.objects.create(
            vendor=self.vendor,
            customer_name="Test",
            district=self.district,
            address="Test",
            phone_number="1234567890",
            total_amount=1000,
            advance_amount=200
        )

        response = self.client.post(
            self.add_payment_url(booking.id),
            {"amount": "300"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Payment.objects.count(), 1)

    # =========================
    # PAYMENT EXCEEDS TOTAL
    # =========================
    def test_payment_exceeds_total(self):

        booking = Booking.objects.create(
            vendor=self.vendor,
            customer_name="Test",
            district=self.district,
            address="Test",
            phone_number="1234567890",
            total_amount=500,
            advance_amount=0
        )

        response = self.client.post(
            self.add_payment_url(booking.id),
            {"amount": "1000"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # =========================
    # UPDATE BOOKING
    # =========================
    def test_update_booking(self):

        booking = Booking.objects.create(
            vendor=self.vendor,
            customer_name="Old",
            district=self.district,
            address="Old Address",
            phone_number="1234567890",
            total_amount=1000,
        )

        response = self.client.put(
            self.update_url(booking.id),
            {
                "customer_name": "Updated",
                "district": self.district.id,
                "address": "New Address",
                "phone_number": "1234567890",
                "total_amount": "1000.00"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        booking.refresh_from_db()
        self.assertEqual(booking.customer_name, "Updated")

    # =========================
    # DELETE BOOKING
    # =========================
    def test_delete_booking(self):

        booking = Booking.objects.create(
            vendor=self.vendor,
            customer_name="Test",
            district=self.district,
            address="Test",
            phone_number="1234567890",
            total_amount=1000,
        )

        response = self.client.delete(self.delete_url(booking.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        booking.refresh_from_db()
        self.assertTrue(booking.is_deleted)

    # =========================
    # TODAY FILTER
    # =========================
    def test_today_filter(self):

        booking = Booking.objects.create(
            vendor=self.vendor,
            customer_name="Today",
            district=self.district,
            address="Test",
            phone_number="1234567890",
            total_amount=1000,
        )

        booking.dates.create(event_date=date.today())

        response = self.client.get(self.list_url + "?type=today")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # =========================
    # SECURITY TEST
    # =========================
    def test_other_vendor_cannot_access(self):

        other_user = User.objects.create_user(
            username="other@test.com",
            password="password123"
        )

        other_vendor = Vendor.objects.create(
            user=other_user,
            name="Other",
            email="other@test.com",
            contact_number="9999999999",
            whatsapp_number="9999999999",
            years_of_experience=2,
            category=self.category,
            joining_date=date.today()
        )

        booking = Booking.objects.create(
            vendor=other_vendor,
            customer_name="Private",
            district=self.district,
            address="Test",
            phone_number="1234567890",
            total_amount=1000,
        )

        response = self.client.delete(self.delete_url(booking.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_calendar_api_returns_booked_dates(self):

    # ----------------------------
    # CREATE BOOKING WITH DATE
    # ----------------------------
    booking = Booking.objects.create(
        vendor=self.vendor,
        customer_name="Calendar User",
        district=self.district,
        address="Test Address",
        phone_number="1234567890",
        total_amount=1000,
        advance_amount=200
    )

    event_date = date.today() + timedelta(days=2)

    booking_date = booking.dates.create(event_date=event_date)

    booking_date.slots.create(
        start_time="10:00:00",
        end_time="12:00:00"
    )

    # ----------------------------
    # CALL CALENDAR API
    # ----------------------------
    url = reverse("booking-calendar")
    response = self.client.get(url)

    # ----------------------------
    # ASSERT RESPONSE
    # ----------------------------
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    data = response.json()

    # date must exist in response
    self.assertIn(str(event_date), data)

    # booking must be inside that date
    self.assertEqual(len(data[str(event_date)]), 1)

    booking_data = data[str(event_date)][0]

    self.assertEqual(booking_data["customer_name"], "Calendar User")
    self.assertEqual(booking_data["payment_status"], "PARTIAL")
    self.assertEqual(booking_data["event_status"], "UPCOMING")

    # slots validation
    self.assertEqual(len(booking_data["slots"]), 1)
    self.assertEqual(booking_data["slots"][0]["start_time"], "10:00:00")

def test_calendar_only_shows_vendor_bookings(self):

    # ----------------------------
    # OTHER VENDOR
    # ----------------------------
    other_user = User.objects.create_user(
        username="other@test.com",
        password="password123"
    )

    other_vendor = Vendor.objects.create(
        user=other_user,
        name="Other Vendor",
        email="other@test.com",
        contact_number="9999999999",
        whatsapp_number="9999999999",
        years_of_experience=2,
        category=self.category,
        joining_date=date.today()
    )

    # ----------------------------
    # OTHER BOOKING (NOT CURRENT USER)
    # ----------------------------
    other_booking = Booking.objects.create(
        vendor=other_vendor,
        customer_name="Hacker Data",
        district=self.district,
        address="Hidden",
        phone_number="1111111111",
        total_amount=1000
    )

    other_date = other_booking.dates.create(
        event_date=date.today() + timedelta(days=5)
    )

    other_date.slots.create(
        start_time="09:00:00",
        end_time="10:00:00"
    )

    # ----------------------------
    # CALL CALENDAR API
    # ----------------------------
    url = reverse("booking-calendar")
    response = self.client.get(url)

    data = response.json()

    # ----------------------------
    # ASSERT CURRENT VENDOR ONLY DATA
    # ----------------------------
    for date_key, bookings in data.items():
        for b in bookings:
            self.assertNotEqual(b["customer_name"], "Hacker Data")