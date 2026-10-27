from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["status"]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = [
            "id",
            "customer",
            "price_per_day",
            "total_price",
            "status",
        ]

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        car = attrs.get("car")

        # Handle partial updates safely.
        if self.instance:
            start_date = start_date or self.instance.start_date
            end_date = end_date or self.instance.end_date
            car = car or self.instance.car

        if start_date and start_date < timezone.localdate():
            raise serializers.ValidationError({
                "start_date": "The start date cannot be in the past."
            })

        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError({
                "end_date": "The end date must be after the start date."
            })

        if car:
            if car.status != "available":
                raise serializers.ValidationError({
                    "car": "This car is not available for booking."
                })

            request = self.context.get("request")

            if request and car.owner_id == request.user.id:
                raise serializers.ValidationError({
                    "car": "You cannot book your own car."
                })

            if start_date and end_date:
                overlapping = Booking.objects.filter(
                    car=car,
                    status="confirmed",
                    start_date__lt=end_date,
                    end_date__gt=start_date,
                )

                # Exclude this booking when updating an existing one.
                if self.instance:
                    overlapping = overlapping.exclude(
                        pk=self.instance.pk
                    )

                if overlapping.exists():
                    raise serializers.ValidationError({
                        "non_field_errors": [
                            "This car is already booked for the selected dates."
                        ]
                    })

        return attrs

    def create(self, validated_data):
        car = validated_data["car"]
        days = (
            validated_data["end_date"] -
            validated_data["start_date"]
        ).days

        validated_data["price_per_day"] = car.price_per_day
        validated_data["total_price"] = car.price_per_day * days
        validated_data["customer"] = self.context["request"].user

        return super().create(validated_data)
