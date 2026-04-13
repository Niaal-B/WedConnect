from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [

    # schema JSON
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),


    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    # Redoc UI (clean docs view)
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ), 
    
    path("admin/", admin.site.urls),

    # API v1
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/vendors/", include("vendors.urls")),

    # JWT
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Bookings
    path("api/v1/bookings/", include("bookings.urls")),
]