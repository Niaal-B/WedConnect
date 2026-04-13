# bookings/models.py

from django.db import models
from django.db.models import Sum
from datetime import date
from vendors.models import Vendor, District


# =========================
# MAIN BOOKING
# =========================
class Booking(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="bookings")

    customer_name = models.CharField(max_length=150)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True,related_name="vendor_bookings")

    address = models.TextField()

    phone_number = models.CharField(max_length=15)
    alternative_phone_number = models.CharField(max_length=15, blank=True, null=True)

    map_url = models.URLField(blank=True, null=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False)

    # ---------------- PAYMENT ----------------
    @property
    def total_paid(self):
        return self.payments.aggregate(total=Sum("amount"))["total"] or 0

    @property
    def balance_amount(self):
        return self.total_amount - self.total_paid

    @property
    def payment_status(self):
        if self.total_paid == 0:
            return "NOT_PAID"
        elif self.total_paid < self.total_amount:
            return "PARTIAL"
        return "PAID"

    # ---------------- EVENT STATUS ----------------
    @property
    def event_status(self):
        today = date.today()

        dates = list(self.dates.values_list("event_date", flat=True))

        if not dates:
            return "UNKNOWN"

        min_date = min(dates)
        max_date = max(dates)

        if min_date <= today <= max_date:
            return "TODAY"
        elif today < min_date:
            return "UPCOMING"
        else:
            return "PAST"

    def __str__(self):
        return f"{self.customer_name} - {self.vendor.name}"


# =========================
# MULTIPLE EVENT DATES
# =========================
class BookingDate(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="dates")
    event_date = models.DateField()

    def __str__(self):
        return f"{self.event_date}"


# =========================
# TIME SLOTS FOR EACH EVENT DATE
# =========================
class BookingSlot(models.Model):
    booking_date = models.ForeignKey(BookingDate, on_delete=models.CASCADE, related_name="slots")

    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


# =========================
# PAYMENTS 
# =========================
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} - {self.booking.customer_name}"