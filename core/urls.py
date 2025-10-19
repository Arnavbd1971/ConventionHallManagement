from django.urls import path, include
from .views import customerSignupView, centerOwnerSignupView, home, centerDetail, verify_email, WebConfigurationView, \
    SliderImagesFormPartialView

app_name = "core"

urlpatterns =[
    path("", home, name="home"),
    path("center-detail/<int:pk>/", centerDetail, name="center_detail"),
    path("webconfig/", WebConfigurationView.as_view(), name="webconfig"),
    path("slider-image-form/", SliderImagesFormPartialView.as_view(), name="slider_image_form_partial"),

    path("signup/customer/", customerSignupView, name="signup_customer"),
    path("signup/center-owner/", centerOwnerSignupView, name="signup_center_owner"),
    path("verify-email/", verify_email, name="verify_email"),

    path("accounts/", include("django.contrib.auth.urls")),
]
