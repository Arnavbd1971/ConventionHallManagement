from django.urls import path
from .views import (
    CenterListView,
    CenterCreateView,
    CenterDetailView,
    HallFormPartialView,
    HallListView,
    # HallCreateView,
    HallUpdateView,
    # HallDeleteView, RentFormPartialView,
    dash_board_view, CenterUpdateView, CenterDeleteView, HallImagesFormPartialView,
    HallDetailView, check_existing_data, AmenityListView, AmenityCreateView, AmenityDetailView, AmenityUpdateView,
    AmenityDeleteView
)



urlpatterns = [
    path("dashboard/", dash_board_view, name="dashboard"),

    # centers urls
    path("centers/", CenterListView.as_view(), name="center_list"),
    path("centers/create/", CenterCreateView.as_view(), name="center_create"),
    path("centers/<int:pk>/", CenterDetailView.as_view(), name="center_detail"),
    path("centers/<int:pk>/edit/", CenterUpdateView.as_view(), name="center_update"),
    path("centers/<int:pk>/delete/", CenterDeleteView.as_view(), name="center_delete"),
    path("centers/hall-form/", HallFormPartialView.as_view(), name="hall_form_partial"),
    path("centers/hall-image-form/", HallImagesFormPartialView.as_view(), name="hall_image_form_partial"),
    path("centers/check-data/", check_existing_data, name="check_existing_data"),

    # halls urls
    path("halls/", HallListView.as_view(), name="hall_list"),
    path("halls/<int:pk>/", HallDetailView.as_view(), name="hall_detail"),
    path("halls/<int:pk>/edit/", HallUpdateView.as_view(), name="hall_edit"),

    # Amenity URLs
    path("amenities/", AmenityListView.as_view(), name="amenity_list"),
    path("amenities/create/", AmenityCreateView.as_view(), name="amenity_create"),
    path("amenities/<int:pk>/", AmenityDetailView.as_view(), name="amenity_detail"),
    path("amenities/<int:pk>/edit/", AmenityUpdateView.as_view(), name="amenity_update"),
    path("amenities/<int:pk>/delete/", AmenityDeleteView.as_view(), name="amenity_delete"),

    # path("halls/create/", HallCreateView.as_view(), name="hall_create"),
    # path("halls/<int:pk>/delete/", HallDeleteView.as_view(), name="hall_delete"),
    # path("halls/rent-form/", RentFormPartialView.as_view(), name="rent_form_partial"),
    # path("halls/hall-image-form/", HallImagesFormPartialView.as_view(), name="hall_image_form_partial"),
]
