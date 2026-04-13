from django.urls import path
from .views import *

urlpatterns = [
    # CATEGORY
    path("categories/", CategoryListCreateView.as_view()),
    path("categories/<int:pk>/", CategoryDetailView.as_view()),

    # STATES
    path("states/", StateListView.as_view()),

    # DISTRICTS
    path("districts/", DistrictListView.as_view()),


 # CREATE
    path("vendors/create/", VendorCreateView.as_view()),

    # LIST
    path("vendors/", VendorListView.as_view()),

    # UPDATE
    path("vendors/<int:pk>/", VendorDetailUpdateView.as_view()),

    # DEACTIVATE
    path("vendors/<int:pk>/deactivate/", VendorDeactivateView.as_view()),

    # ACTIVATE
    path("vendors/<int:pk>/activate/", VendorActivateView.as_view()),


    # Vendor Login
    path("vendors/login/", VendorLoginView.as_view()),

    # Vendor Me
    path("vendors/me/", VendorMeView.as_view()),

    # Vendor Forgot Password
    path("vendors/forgot-password/", VendorForgotPasswordView.as_view()),

    # Vendor Reset Password
    path("vendors/reset-password/<uid>/<token>/", VendorResetPasswordView.as_view()),
]