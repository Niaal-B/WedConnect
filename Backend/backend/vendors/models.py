from django.db import models
from django.contrib.auth.models import User


# =========================
# CATEGORY
# =========================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# STATE 
# =========================
class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# =========================
# DISTRICT 
# =========================
class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="districts")

    def __str__(self):
        return f"{self.name} - {self.state.name}"


# =========================
# VENDOR 
# =========================
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor_profile")

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True,default="")

    contact_number = models.CharField(max_length=15, unique=True)
    alternative_number = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15)

    years_of_experience = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="vendors")

    districts = models.ManyToManyField(District, related_name="vendors")

    instagram_url = models.URLField(blank=True, null=True)

    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# =========================
# BOOKING
# =========================
class Booking(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")

    customer_name = models.CharField(max_length=150)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)

    address = models.TextField()

    phone_number = models.CharField(max_length=15)
    alternative_phone_number = models.CharField(max_length=15, blank=True, null=True)

    map_url = models.URLField(blank=True, null=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.vendor.username}"


# =========================
# BOOKING EVENTS (MULTIPLE DATES + TIME)
# =========================
class BookingEvent(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="events")

    event_date = models.DateField()

    # Flexible slot
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.event_date} ({self.start_time} - {self.end_time})"


# =========================
# PAYMENTS (TRACK MULTIPLE PAYMENTS)
# =========================
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} - {self.booking.customer_name}"