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
# STATE (NEW - IMPORTANT)
# =========================
class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# =========================
# DISTRICT (FIXED RELATION)
# =========================
class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="districts")

    def __str__(self):
        return f"{self.name} - {self.state.name}"


# =========================
# VENDOR (FIXED)
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