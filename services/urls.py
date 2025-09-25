from django.urls import path
from .views import (
    HallListView,
    HallCreateView,
    HallUpdateView,
    HallDeleteView, RentFormPartialView,
)

urlpatterns = [
    path("halls/", HallListView.as_view(), name="hall_list"),
    path("halls/create/", HallCreateView.as_view(), name="hall_create"),
    path("halls/<int:pk>/edit/", HallUpdateView.as_view(), name="hall_edit"),
    path("halls/<int:pk>/delete/", HallDeleteView.as_view(), name="hall_delete"),
    path("halls/rent-form/", RentFormPartialView.as_view(), name="rent_form_partial"),
]
