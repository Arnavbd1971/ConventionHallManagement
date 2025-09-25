from django.urls import path
from .views import (
    HallListView,
    HallCreateView,
    HallUpdateView,
    HallDeleteView, RentFormPartialView, HallImagesFormPartialView, dash_board_view, HallDetailView,
)

urlpatterns = [
    path("dashboard/", dash_board_view, name="daashboard"),

    path("halls/", HallListView.as_view(), name="hall_list"),
    path("halls/create/", HallCreateView.as_view(), name="hall_create"),
    path("halls/<int:pk>/", HallDetailView.as_view(), name="hall_detail"),
    path("halls/<int:pk>/edit/", HallUpdateView.as_view(), name="hall_edit"),
    path("halls/<int:pk>/delete/", HallDeleteView.as_view(), name="hall_delete"),
    path("halls/rent-form/", RentFormPartialView.as_view(), name="rent_form_partial"),
    path("halls/hall-image-form/", HallImagesFormPartialView.as_view(), name="hall_image_form_partial"),
]
