from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        if not user.is_superuser:
            raise serializers.ValidationError("Access denied. Superuser only.")

        data["user"] = user
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]