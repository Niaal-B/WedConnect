from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import AdminLoginSerializer, UserDetailSerializer


def get_tokens_for_user(user):
    """Generate JWT access and refresh tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class AdminLoginView(APIView):
    permission_classes = [AllowAny]
    """
    POST /api/accounts/login/
    Login with superuser credentials and receive JWT tokens.
    """

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = get_tokens_for_user(user)

            return Response(
                {
                    "message": "Login successful.",
                    "user": UserDetailSerializer(user).data,
                    "tokens": tokens,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLogoutView(APIView):
    """
    POST /api/accounts/logout/
    Blacklist the refresh token to log out.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout successful."},
                status=status.HTTP_205_RESET_CONTENT,
            )

        except Exception as e:
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AdminMeView(APIView):
    """
    GET /api/accounts/me/
    Returns the currently authenticated superuser's details.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

    def get(self, request):
        if not request.user.is_superuser:
            return Response(
                {"error": "Access denied. Superuser only."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)