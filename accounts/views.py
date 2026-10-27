from django.db.models import F
from django.db import transaction
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Balance_Recharge, UserBalance
from rest_framework.permissions import IsAuthenticated
from .serializers import SignupSerializer, BalanceRechargeSerializer, ProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()





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


class Profile(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

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

            balance, created = UserBalance.objects.get_or_create(
                user=request.user,
                defaults={"balance": 0}
            )

            UserBalance.objects.filter(pk=balance.pk).update(
                balance=F("balance") + ticket.balance
            )

            amount = ticket.balance
            ticket.is_used = True
            ticket.save(update_fields=["is_used"])

        return Response(
            {
                "message": "Ticket redeemed successfully.",
                "amount": str(amount),
            },
            status=status.HTTP_200_OK
        )