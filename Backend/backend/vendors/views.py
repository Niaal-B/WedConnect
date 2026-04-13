from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import StateSerializer, DistrictSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView
from django.contrib.auth import authenticate
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import CategorySerializer
from .permissions import IsAdminUserOnly
from .serializers import VendorSerializer
from django.core.mail import send_mail
from django.db import transaction
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
import os



# =========================
# LIST + CREATE
# =========================
class CategoryListCreateView(APIView):
    permission_classes = [IsAdminUserOnly]

    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Category created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================
# DETAIL / UPDATE / DELETE
# =========================
class CategoryDetailView(APIView):
    permission_classes = [IsAdminUserOnly]

    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Category updated successfully", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.is_active = False
        category.save()

        return Response(
            {"message": "Category deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    

# =========================
# STATES API
# =========================
class StateListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)


# =========================
# DISTRICTS API (FILTER BY STATE)
# =========================
class DistrictListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        state_name = request.query_params.get("state")

        districts = District.objects.all()

        if state_name:
            districts = districts.filter(state__name__iexact=state_name)

        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data)
    


class VendorCreateView(APIView):
    permission_classes = [IsAdminUserOnly]

    @transaction.atomic
    def post(self, request):
        serializer = VendorSerializer(data=request.data)

        if serializer.is_valid():
            vendor = serializer.save()

            password = vendor.raw_password

            # EMAIL
            send_mail(
                subject="Your Vendor Account is Ready",
                message=f"""
                Hello {vendor.name},

                Your vendor account has been created successfully.

                LOGIN DETAILS:
                Username: {vendor.user.username}
                Password: {password}

                Please login and change your password immediately.

                Regards,
                Team
                """,
                from_email=os.getenv("DEFAULT_FROM_EMAIL"),
                recipient_list=[vendor.email],
                fail_silently=False,
            )

            return Response({
                "message": "Vendor created successfully",
                "vendor_id": vendor.id,
                "username": vendor.user.username,
                "email": vendor.email
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VendorListView(ListAPIView):
    permission_classes = [IsAdminUserOnly]
    queryset = Vendor.objects.all().order_by("-created_at")
    serializer_class = VendorSerializer
    


class VendorLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            return Response({"message": "Invalid credentials"}, status=401)

        # 🚨 CHECK VENDOR STATUS
        try:
            vendor = user.vendor_profile
        except:
            return Response({"message": "Vendor not found"}, status=404)

        if not vendor.is_active:
            return Response({
                "message": "Your account is deactivated. Contact admin."
            }, status=403)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
    

class VendorDeactivateView(APIView):
    permission_classes = [IsAdminUserOnly]
    def patch(self, request, pk):

        try:
            vendor = Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response({"message": "Vendor not found"}, status=404)

        vendor.is_active = False
        vendor.save()

        return Response({
            "message": "Vendor deactivated successfully"
        }, status=200)
    

class VendorActivateView(APIView):
    permission_classes = [IsAdminUserOnly]

    def patch(self, request, pk):
        try:
            vendor = Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response({"message": "Vendor not found"}, status=404)

        vendor.is_active = True
        vendor.save()

        return Response({"message": "Vendor activated"})
    
class VendorDetailUpdateView(RetrieveUpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUserOnly]


class VendorMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendor = request.user.vendor_profile
        return Response(VendorSerializer(vendor).data)
    
class VendorForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "If this email exists, a reset link has been sent."},
                status=200,
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"

        send_mail(
            subject="Reset Your Password",
            message=f"Click the link to reset your password:\n{reset_link}",
            from_email=os.getenv("DEFAULT_FROM_EMAIL"),
            recipient_list=[email],
        )

        return Response(
            {"message": "Password reset link sent to email."},
            status=200,
        )
    




class VendorResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uid, token):
        password = request.data.get("password")

        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"error": "Invalid link"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Token expired or invalid"}, status=400)

        user.set_password(password)
        user.save()

        return Response({"message": "Password reset successful"})