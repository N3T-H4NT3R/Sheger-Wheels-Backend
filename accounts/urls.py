from django.urls import path
from .views import SignupView, Refunded, RechargeBalance
from rest_framework_simplejwt.views import TokenObtainPairView



urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("signup/", SignupView.as_view(), name="signup"),
    path("refunded/", Refunded.as_view(), name="refunded"),
    path("rechareg/", RechargeBalance.as_view(), name="rechareg"),
]