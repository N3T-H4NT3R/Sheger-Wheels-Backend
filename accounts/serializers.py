from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Balance_Recharge


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data,
            is_staff=False,
            is_superuser=False
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(source="balance_account.balance", max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "balance"]

class BalanceRechargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance_Recharge
        fields = ["code",]
        read_only_fields = ["code"]