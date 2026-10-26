from django.db import models
from django.contrib.auth.models import User



class Car(models.Model):

    class FuelType(models.TextChoices):
        DIESEL = "diesel", "Diesel"
        PETROL = "petrol", "Petrol"
        ELECTRIC = "electric", "Electric"
        HYBRID = "hybrid", "Hybrid"

    class Transmission(models.TextChoices):
        MANUAL = "manual", "Manual"
        AUTOMATIC = "automatic", "Automatic"

    class CarStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        AVAILABLE = "available", "Available"
        RENTED = "rented", "Rented"
        MAINTENANCE = "maintenance", "Maintenance"
        REJECTED = "rejected", "Rejected"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars")
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    fuel_type = models.CharField(max_length=10, choices=FuelType.choices, default=FuelType.PETROL)
    transmission = models.CharField(max_length=10, choices=Transmission.choices, default=Transmission.MANUAL)
    seats = models.PositiveSmallIntegerField(default=5)
    color = models.CharField(max_length=30, blank=True)
    body_type = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=50, default="Addis Ababa")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=CarStatus.choices, default=CarStatus.PENDING)
    mileage = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="cars/gallery/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car}"