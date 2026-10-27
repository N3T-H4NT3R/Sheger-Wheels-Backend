from django.db import models
from django.conf import settings


class Balance_Recharge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=14, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.balance} ETB"


class UserBalance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="balance_account")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user} - {self.balance}"