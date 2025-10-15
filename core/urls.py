from django.urls import path, include
from .views import customerSignupView, centerOwnerSignupView, home, hallDetail, verify_email, WebConfigurationView, \
    SliderImagesFormPartialView

app_name = "core"

urlpatterns =[
    path("", home, name="home"),
    path("hall-detail/<int:pk>/", hallDetail, name="hall_detail"),
    path("webconfig/", WebConfigurationView.as_view(), name="webconfig"),
    path("slider-image-form/", SliderImagesFormPartialView.as_view(), name="slider_image_form_partial"),

    path("signup/customer/", customerSignupView, name="signup_customer"),
    path("signup/center-owner/", centerOwnerSignupView, name="signup_center_owner"),
    path("verify-email/", verify_email, name="verify_email"),

    path("accounts/", include("django.contrib.auth.urls")),
]
