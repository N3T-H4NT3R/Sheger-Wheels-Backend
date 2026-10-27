from django.urls import path
from .views import Booking_List_CreateView, BookingStatusUpdateView, OwnerRentalDashboardView



urlpatterns = [
    path("car/", Booking_List_CreateView.as_view(), name="booking-list-create"),
    path("<int:pk>/status/", BookingStatusUpdateView.as_view(),name="booking-status-update"),
    path("dashboard/", OwnerRentalDashboardView.as_view(), name="owner-rental-dashboard"),
]