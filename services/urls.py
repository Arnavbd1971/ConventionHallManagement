from django.urls import path
from .views import (
    CenterListView,
    CenterCreateView,
    CenterDetailView,
    HallFormPartialView,
    HallListView,
    # HallCreateView,
    # HallUpdateView,
    # HallDeleteView, RentFormPartialView, HallImagesFormPartialView,
    dash_board_view, CenterUpdateView,
    # HallDetailView,
)



urlpatterns = [
    path("dashboard/", dash_board_view, name="dashboard"),

    path("centers/", CenterListView.as_view(), name="center_list"),
    path("centers/create/", CenterCreateView.as_view(), name="center_create"),
    path("centers/<int:pk>/", CenterDetailView.as_view(), name="center_detail"),
    path("centers/<int:pk>/edit/", CenterUpdateView.as_view(), name="center_update"),
    path("centers/hall-form/", HallFormPartialView.as_view(), name="hall_form_partial"),
    path("halls/", HallListView.as_view(), name="hall_list"),

    # path("halls/create/", HallCreateView.as_view(), name="hall_create"),
    # path("halls/<int:pk>/", HallDetailView.as_view(), name="hall_detail"),
    # path("halls/<int:pk>/edit/", HallUpdateView.as_view(), name="hall_edit"),
    # path("halls/<int:pk>/delete/", HallDeleteView.as_view(), name="hall_delete"),
    # path("halls/rent-form/", RentFormPartialView.as_view(), name="rent_form_partial"),
    # path("halls/hall-image-form/", HallImagesFormPartialView.as_view(), name="hall_image_form_partial"),
]
