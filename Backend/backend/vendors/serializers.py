from rest_framework import serializers
from .models import Category,Vendor
from .models import State, District
from django.contrib.auth.models import User
import random
import string
from django.db import transaction
from django.contrib.auth import authenticate 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Category name must be at least 3 characters."
            )

        qs = Category.objects.filter(name__iexact=value)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("Category already exists.")

        return value
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source="state.name", read_only=True)

    class Meta:
        model = District
        fields = ["id", "name", "state", "state_name"]



class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True}
        }

    # ---------------- VALIDATIONS ----------------
    def validate_email(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Email already exists")

        if Vendor.objects.filter(email=value).exists():
            raise serializers.ValidationError("Vendor email already exists")

        return value

    def validate_contact_number(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Invalid contact number")
        return value

    def validate_years_of_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience cannot be negative")
        return value

    # ---------------- PASSWORD GENERATOR ----------------
    def generate_password(self):
        return ''.join(random.choices(
            string.ascii_letters + string.digits + "!@#$%", k=10
        ))

    # ---------------- CREATE ----------------
    @transaction.atomic
    def create(self, validated_data):

        districts = validated_data.pop("districts", [])
        email = validated_data.get("email")

        raw_password = self.generate_password()

        # 1. CREATE USER (REAL LOGIN PASSWORD)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=raw_password
        )

        # 2. CREATE VENDOR PROFILE
        vendor = Vendor.objects.create(
            user=user,
            **validated_data
        )

        # 3. ASSIGN M2M
        if districts:
            vendor.districts.set(districts)

        # 4. attach password for response/email only
        vendor.raw_password = raw_password

        return vendor