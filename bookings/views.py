from decimal import Decimal
from .models import Booking
from .utils import generate_ticket_code
from .serializers import BookingSerializer
from rest_framework import generics, permissions
from accounts.models import Balance_Recharge





class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            customer=self.request.user
        ).select_related(
            "car", "customer"
        ).order_by("-created_at")

    def perform_create(self, serializer):
        booking = serializer.save(customer=self.request.user)

        rental_days = (
            booking.end_date - booking.start_date
        ).days

        if rental_days >= 5:
            refund_percent = Decimal(rental_days)

            refund_amount = (
                Decimal(str(booking.total_price))
                * refund_percent
                / Decimal("100")
            ).quantize(Decimal("0.01"))

            Balance_Recharge.objects.create(
                user=self.request.user,
                code=generate_ticket_code(),
                balance=refund_amount
            )


class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            customer=self.request.user
        ).select_related("car", "customer")
