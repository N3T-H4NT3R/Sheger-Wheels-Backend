from django.db import transaction
from .models import Balance_Recharge
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import SignupSerializer, BalanceRechargeSerializer




class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Account created successfully.",
                "user": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class Refunded(generics.ListAPIView):
    serializer_class = BalanceRechargeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Balance_Recharge.objects.filter(
            user=self.request.user
        ).order_by("-id")

class RechargeBalance(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")

        if not code:
            return Response(
                {"error": "Ticket code is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            try:
                ticket = Balance_Recharge.objects.select_for_update().get(
                    code=code,
                    user=request.user,
                    is_used=False
                )
            except Balance_Recharge.DoesNotExist:
                return Response(
                    {"error": "Invalid ticket or ticket already used."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            ticket.is_used = True
            ticket.save(update_fields=["is_used"])

        return Response(
            {
                "message": "Ticket redeemed successfully.",
                "amount": str(ticket.balance)
            },
            status=status.HTTP_200_OK
        )