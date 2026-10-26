from .models import Car
from .serializers import CarSerializer
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied




class CarListCreateView(generics.ListCreateAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.filter(
            status=Car.CarStatus.AVAILABLE
        ).order_by("-created_at")

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            status=Car.CarStatus.PENDING
        )


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        if self.get_object().owner != self.request.user:
            raise PermissionDenied(
                "You can only update your own cars."
            )
        serializer.save(
            owner=self.get_object().owner
        )

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied(
                "You can only delete your own cars."
            )
        instance.delete()
