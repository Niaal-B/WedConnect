# bookings/serializers.py

from rest_framework import serializers
from .models import Booking, BookingDate, BookingSlot, Payment


class BookingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingSlot
        fields = ["start_time", "end_time"]

    def validate(self, data):
        if data["start_time"] >= data["end_time"]:
            raise serializers.ValidationError("End time must be after start time")
        return data


class BookingDateSerializer(serializers.ModelSerializer):
    slots = BookingSlotSerializer(many=True)

    class Meta:
        model = BookingDate
        fields = ["event_date", "slots"]

    def validate_event_date(self, value):
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("Event date cannot be in past")
        return value


class BookingCreateSerializer(serializers.ModelSerializer):
    dates = BookingDateSerializer(many=True)

    class Meta:
        model = Booking
        fields = [
            "customer_name",
            "district",
            "address",
            "phone_number",
            "alternative_phone_number",
            "map_url",
            "total_amount",
            "advance_amount",
            "dates",
        ]

    # ---------------- VALIDATIONS ----------------
    def validate_phone_number(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Invalid phone number")
        return value

    def validate(self, data):
        if data["advance_amount"] > data["total_amount"]:
            raise serializers.ValidationError("Advance cannot exceed total amount")
        return data

    # ---------------- CREATE ----------------
    def create(self, validated_data):
        request = self.context["request"]
        vendor = request.user.vendor_profile

        dates_data = validated_data.pop("dates")

        booking = Booking.objects.create(
            vendor=vendor,
            **validated_data
        )

        # SAVE DATES + SLOTS
        for date_data in dates_data:
            slots_data = date_data.pop("slots")

            booking_date = BookingDate.objects.create(
                booking=booking,
                **date_data
            )

            for slot in slots_data:
                BookingSlot.objects.create(
                    booking_date=booking_date,
                    **slot
                )

        # INITIAL PAYMENT
        if booking.advance_amount > 0:
            Payment.objects.create(
                booking=booking,
                amount=booking.advance_amount
            )

        return booking
    
class BookingListSerializer(serializers.ModelSerializer):
    total_paid = serializers.SerializerMethodField()
    balance_amount = serializers.SerializerMethodField()
    payment_status = serializers.CharField(read_only=True)
    event_status = serializers.CharField(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"

    def get_total_paid(self, obj):
        return obj.total_paid

    def get_balance_amount(self, obj):
        return obj.balance_amount
    
class AddPaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        booking = self.context["booking"]

        if data["amount"] <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")

        if booking.total_paid + data["amount"] > booking.total_amount:
            raise serializers.ValidationError("Exceeds total amount")

        return data
    
class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "customer_name",
            "district",
            "address",
            "phone_number",
            "alternative_phone_number",
            "map_url",
            "total_amount",
        ]

    def validate_total_amount(self, value):
        booking = self.instance

        if booking and value < booking.total_paid:
            raise serializers.ValidationError(
                "Total amount cannot be less than already paid"
            )
        return value