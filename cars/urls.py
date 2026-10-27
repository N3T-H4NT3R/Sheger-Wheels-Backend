from django.urls import path
from .views import CarDetailView, CarListCreateView, OwnerCarListView


urlpatterns = [
    path("car/", CarListCreateView.as_view(), name="car-list-create"),
    path("<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("car/", OwnerCarListView.as_view(), name="my-cars",
    ),
]