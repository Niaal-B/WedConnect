from django.urls import path
from .views import *

urlpatterns = [
    path("list/", VendorBookingListView.as_view(), name="vendor-bookings"),
    path("create/", BookingCreateView.as_view(), name="booking-create"),
    path("update/<int:pk>/", BookingUpdateView.as_view(), name="booking-update"),
    path("delete/<int:pk>/", BookingDeleteView.as_view(), name="booking-delete"),
    path("add-payment/<int:pk>/", AddPaymentView.as_view(), name="booking-add-payment"),

    path("calendar/", BookingCalendarView.as_view(), name="booking-calendar"),
]