from .models import Booking
from decimal import Decimal
from django.db import transaction
from .utils import generate_ticket_code
from accounts.models import Balance_Recharge
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .serializers import BookingSerializer, BookingStatusSerializer
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated




class Booking_List_CreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            customer=self.request.user
        ).select_related(
            "car", "customer"
        ).order_by("-id")

    @transaction.atomic
    def perform_create(self, serializer):
        booking = serializer.save(customer=self.request.user)

        rental_days = (
            booking.end_date - booking.start_date
        ).days

        if rental_days >= 5:
            refund_percent = Decimal(rental_days)

            refund_amount = (
                booking.total_price
                * refund_percent
                / Decimal("100")
            ).quantize(Decimal("0.01"))

            if refund_amount > 0:
                Balance_Recharge.objects.create(
                    user=self.request.user,
                    code=generate_ticket_code(),
                    balance=refund_amount
                )


class BookingStatusUpdateView(generics.UpdateAPIView):
    serializer_class = BookingStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch", "head", "options"]

    def get_queryset(self):
        return Booking.objects.filter(
            car__owner=self.request.user
        )

    def perform_update(self, serializer):
        booking = serializer.instance
        new_status = serializer.validated_data["status"]

        allowed_transitions = {
            Booking.BookingStatus.PENDING: [
                Booking.BookingStatus.CONFIRMED,
                Booking.BookingStatus.CANCELLED,
            ],
            Booking.BookingStatus.CONFIRMED: [
                Booking.BookingStatus.CANCELLED,
                Booking.BookingStatus.COMPLETED,
            ],
        }

        if new_status not in allowed_transitions.get(
            booking.status, []
        ):
            raise ValidationError({
                "status": (
                    f"Cannot change status from "
                    f"'{booking.status}' to '{new_status}'."
                )
            })

        serializer.save()


class OwnerRentalDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(
            car__owner=request.user
        )

        rented = bookings.filter(
            status__in=[
                Booking.BookingStatus.CONFIRMED,
                Booking.BookingStatus.COMPLETED,
            ]
        )

        total_income = (
            rented.aggregate(
                total=Sum("total_price")
            )["total"]
            or Decimal("0.00")
        )

        return Response({
            "total_cars_rented": rented.count(),
            "total_income": str(total_income),
            "currency": "ETB",
            "pending_bookings": bookings.filter(
                status=Booking.BookingStatus.PENDING
            ).count(),
            "confirmed_bookings": bookings.filter(
                status=Booking.BookingStatus.CONFIRMED
            ).count(),
            "completed_bookings": bookings.filter(
                status=Booking.BookingStatus.COMPLETED
            ).count(),
        })