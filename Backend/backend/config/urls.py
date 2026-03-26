from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    # API v1
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/vendors/", include("vendors.urls")),

    # JWT
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]