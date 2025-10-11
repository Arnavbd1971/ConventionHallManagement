from django.urls import path, include
from .views import customerSignupView, centerOwnerSignupView, home, hallDetail, verify_email

urlpatterns =[
    path("", home, name="home"),
    path("hall-detail/<int:pk>/", hallDetail, name="hall_detail"),

    path("signup/customer/", customerSignupView, name="signup_customer"),
    path("signup/center-owner/", centerOwnerSignupView, name="signup_center_owner"),
    path("verify-email/", verify_email, name="verify_email"),

    path("accounts/", include("django.contrib.auth.urls")),
]
