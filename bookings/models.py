from cars.models import Car
from django.db import models
from django.conf import settings



class Booking(models.Model):

    class BookingStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    car = models.ForeignKey(Car, on_delete=models.PROTECT,related_name="bookings")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)

    def __str__(self):
        return f"Booking #{self.pk} - {self.car}"
