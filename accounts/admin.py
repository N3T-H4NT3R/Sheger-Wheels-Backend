from django.contrib import admin
from cars.models import Car, CarImage
from bookings.models import Booking
from .models import Balance_Recharge, UserBalance
# Register your models here.


admin.site.register(Car)
admin.site.register(Booking)
admin.site.register(CarImage)
admin.site.register(UserBalance)
admin.site.register(Balance_Recharge)