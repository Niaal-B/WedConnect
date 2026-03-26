from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    StateListView,
    DistrictListView,
    VendorCreateView,
    VendorListView,
    VendorDetailUpdateView,
    VendorDeactivateView,
    VendorActivateView,
)

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
]