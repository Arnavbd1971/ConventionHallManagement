from django.urls import path, include
from .views import authView, home, hallDetail

urlpatterns =[
    path("", home, name="home"),
    path("hall-detail/<int:pk>/", hallDetail, name="hall_detail"),

    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
]
