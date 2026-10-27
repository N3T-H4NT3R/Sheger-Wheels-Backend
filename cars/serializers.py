from .models import Car, CarImage
from datetime import date
from rest_framework import serializers



class CarImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CarImage
        fields = ["id", "image"]

    def get_image(self, obj):
        request = self.context.get("request")

        if not obj.image:
            return None

        url = obj.image.url

        if request:
            return request.build_absolute_uri(url)

        return url

class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Car
        fields = "__all__"

        read_only_fields = ["id", "owner", "images", "status"]

    def validate_year(self, value):
        current_year = date.today().year

        if value < 1886 or value > current_year + 1:
            raise serializers.ValidationError(
                "Enter a valid car manufacturing year."
            )

        return value

    def validate_price_per_day(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price per day must be greater than zero."
            )

        return value

    def validate_seats(self, value):
        if value < 1 or value > 100:
            raise serializers.ValidationError(
                "Seats must be between 1 and 100."
            )

        return value
