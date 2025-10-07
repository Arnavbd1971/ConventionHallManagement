from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Center, Hall, HallImage, Amenity
from .forms import CenterForm, AmenityForm
from .forms import (
                    CenterForm,
                    HallForm,
                    HallFormSet,
                    HallImagesFormSet,
                    HallImageForm
                    )
from django.views.decorators.http import require_GET
from django.contrib.messages.views import SuccessMessageMixin

def dash_board_view(request):
    return render(request, "adminlte/dashboard.html", {})

class CenterListView(ListView):
    model = Center
    template_name = "adminlte/center_list.html"
    context_object_name = "centers"

    def get_queryset(self):
        return Center.objects.exclude(status='deleted').order_by('-id')

class CenterCreateView(View):
    template_name = "adminlte/center_form.html"
    success_url = reverse_lazy("services:center_list")

    def get(self, request):
        center_form = CenterForm()
        hall_formset = HallFormSet(queryset=Hall.objects.none(), prefix="hall")
        hall_images_formset = HallImagesFormSet(queryset=HallImage.objects.none(), prefix="hallimage")

        return render(request, self.template_name, {
            "center_form": center_form,
            "hall_formset": hall_formset,
            "hall_images_formset": hall_images_formset,
        })

    def post(self, request):
        center_form = CenterForm(request.POST)
        hall_formset = HallFormSet(request.POST, queryset=Hall.objects.none(), prefix="hall")
        hall_images_formset = HallImagesFormSet(request.POST, request.FILES, queryset=HallImage.objects.none(),
                                                prefix="hallimage")

        if center_form.is_valid() and hall_formset.is_valid() and hall_images_formset.is_valid():
            # Save Center first
            center = center_form.save()

            # Save each Hall and link to Center
            halls = hall_formset.save(commit=False)
            for hall in halls:
                hall.center = center
                hall.is_active = True
                hall.save()

            # Save each Hall Images and link to Center
            hall_images = hall_images_formset.save(commit=False)
            for hall_image in hall_images:
                hall_image.center = center
                hall_image.save()

            # Handle deleted halls (if can_delete=True)
            for hall in hall_formset.deleted_objects:
                hall.delete()

            # Handle deleted hall Images (if can_delete=True)
            for hall_image in hall_images_formset.deleted_objects:
                hall_image.delete()

            messages.success(request, "Center created successfully!")
            return redirect(self.success_url)

        # Collect form errors into Django messages
        for field, errors in center_form.errors.items():
            for error in errors:
                messages.error(request, f"{field.capitalize()}: {error}")

        for i, form_errors in enumerate(hall_formset.errors, start=1):
            for field, errors in form_errors.items():
                for error in errors:
                    messages.error(request, f"Hall {i} → {field.capitalize()}: {error}")

        for error in hall_formset.non_form_errors():
            messages.error(request, error)

        for i, form_errors in enumerate(hall_images_formset.errors, start=1):
            for field, errors in form_errors.items():
                for error in errors:
                    messages.error(request, f"Hall Images {i} → {field.capitalize()}: {error}")

        for error in hall_images_formset.non_form_errors():
            messages.error(request, error)

        return render(request, self.template_name, {
            "center_form": center_form,
            "hall_formset": hall_formset,
            "hall_images_formset": hall_images_formset,
        })

class CenterDetailView(View):
    template_name = "adminlte/center_detail.html"

    def get(self, request, pk):
        center = Center.objects.get(pk=pk)
        hall_formset = HallFormSet(queryset=center.halls.all())
        hall_images_formset = HallImagesFormSet(queryset=center.center_images.all())  # images linked to center

        return render(request, self.template_name, {
            "center": center,
            "hall_formset": hall_formset,
            "hall_images_formset": hall_images_formset,
        })

class CenterUpdateView(View):
    template_name = "adminlte/center_form.html"
    success_url = reverse_lazy("services:center_list")

    def get_object(self, pk):
        return get_object_or_404(Center, pk=pk)

    def get(self, request, pk):
        center = self.get_object(pk)
        center_form = CenterForm(instance=center)
        hall_formset = HallFormSet(queryset=Hall.objects.filter(center=center), prefix="hall")
        hall_images_formset = HallImagesFormSet(queryset=HallImage.objects.filter(center=center), prefix="hallimage")

        # Amenity Form
        amenity_form = AmenityForm()
        all_amenities = Amenity.objects.all()

        return render(request, self.template_name, {
            "center_form": center_form,
            "hall_formset": hall_formset,
            "hall_images_formset": hall_images_formset,
            "amenity_form": amenity_form,
            "all_amenities": all_amenities,
            "center": center,
            "is_edit": True,
        })

    def post(self, request, pk):
        center = self.get_object(pk)
        center_form = CenterForm(request.POST, instance=center)
        hall_formset = HallFormSet(request.POST, queryset=Hall.objects.filter(center=center), prefix="hall")
        hall_images_formset = HallImagesFormSet(request.POST, request.FILES,
                                                queryset=HallImage.objects.filter(center=center), prefix="hallimage")

        # Handle amenities selection
        selected_amenities = request.POST.getlist('amenities')


        if center_form.is_valid() and hall_formset.is_valid() and hall_images_formset.is_valid():
            center = center_form.save()

            # Update amenities
            center.amenities.set(selected_amenities)

            halls = hall_formset.save(commit=False)
            for hall in halls:
                hall.center = center
                hall.is_active = True
                hall.save()

            # Handle deleted halls
            for hall in hall_formset.deleted_objects:
                hall.delete()

            hall_images = hall_images_formset.save(commit=False)
            for hall_image in hall_images:
                hall_image.center = center
                hall_image.save()

            for hall_image in hall_images_formset.deleted_objects:
                hall_image.delete()

            messages.success(request, "Center updated successfully!")
            return redirect(self.success_url)

        # DEBUGGING
        # print("❌ Center form errors:", center_form.errors)
        # print("❌ Hall formset errors:", hall_formset.errors)
        # print("❌ Hall Images formset errors:", hall_images_formset.non_form_errors())
        # print("❌ Non-form errors:", hall_formset.non_form_errors())
        # Handle errors
        for field, errors in center_form.errors.items():
            for error in errors:
                messages.error(request, f"{field.capitalize()}: {error}")

        for i, form_errors in enumerate(hall_formset.errors, start=1):
            for field, errors in form_errors.items():
                for error in errors:
                    messages.error(request, f"Hall {i} → {field.capitalize()}: {error}")

        for error in hall_formset.non_form_errors():
            messages.error(request, error)

        for i, form_errors in enumerate(hall_images_formset.errors, start=1):
            for field, errors in form_errors.items():
                for error in errors:
                    messages.error(request, f"Hall Images {i} → {field.capitalize()}: {error}")

        for error in hall_images_formset.non_form_errors():
            messages.error(request, error)

        # Reload amenities on failed form
        all_amenities = Amenity.objects.all()

        return render(request, self.template_name, {
            "center_form": center_form,
            "hall_formset": hall_formset,
            "hall_images_formset": hall_images_formset,
            "all_amenities": all_amenities,
            "center": center,
            "is_edit": True,
        })

class CenterDeleteView(View):
    success_url = reverse_lazy("services:center_list")

    def post(self, request, pk):
        center = get_object_or_404(Center, pk=pk)

        # Soft delete center
        center.status = "deleted"
        center.save()

        # Soft delete related halls
        Hall.objects.filter(center=center).update(is_active=False)

        messages.success(request, f"Center '{center.name}' has been deleted.")
        return redirect(self.success_url)

@require_GET
def check_existing_data(request):
    name = request.GET.get("name", "").strip()
    address = request.GET.get("address", "").strip()

    hallname = request.GET.get("hallname", "").strip()

    exists = False
    if name:
        exists = Center.objects.filter(name__iexact=name, status="approved").exists()
        return JsonResponse({
            "exists": exists,
            "message": "Center name already exists!" if exists else ""
        })
    if address:
        exists = Center.objects.filter(address__iexact=address, status="approved").exists()
        return JsonResponse({
            "exists": exists,
            "message": "Center address already exists!" if exists else ""
        })
    if hallname:
        exists = Hall.objects.filter(name__iexact=hallname, center__status="approved").exists()
        return JsonResponse({
            "exists": exists,
            "message": "Hall name already exists!" if exists else ""
        })

class HallFormPartialView(View):
    def get(self, request):
        total_forms = int(request.GET.get("hall-TOTAL_FORMS", 0))
        hall_form = HallForm(prefix=f"hall-{total_forms}")

        management_form = (
            f'<input type="hidden" name="hall-TOTAL_FORMS" id="id_hall-TOTAL_FORMS" value="{total_forms + 1}">'
        )
        html = render_to_string("adminlte/hall_form_inline.html", {"hall_form": hall_form})
        return HttpResponse(management_form + html)

class HallImagesFormPartialView(View):
    def get(self, request):
        total_forms = int(request.GET.get("hallimage-TOTAL_FORMS", 0))
        hall_images_form = HallImageForm(prefix=f"hallimage-{total_forms}")

        management_form = (
            f'<input type="hidden" name="hallimage-TOTAL_FORMS" id="id_hallimage-TOTAL_FORMS" value="{total_forms + 1}">'
        )
        html = render_to_string("adminlte/hall_images_form.html", {"hall_image_form": hall_images_form})
        return HttpResponse(management_form + html)

class HallListView(ListView):
    model = Hall
    template_name = "adminlte/hall_list.html"
    context_object_name = "halls"

    def get_queryset(self):
        return Hall.objects.filter(is_active=True).order_by('-id')

class HallDetailView(View):
    template_name = "adminlte/hall_detail.html"

    def get(self, request, pk):
        hall = get_object_or_404(Hall, pk=pk)

        return render(request, self.template_name, {
            "hall": hall
        })

class HallUpdateView(View):
    template_name = "adminlte/hall_form.html"
    success_url = reverse_lazy("services:hall_list")

    def get_object(self, pk):
        return get_object_or_404(Hall, pk=pk)

    def get(self, request, pk):
        hall = self.get_object(pk)
        hall_form = HallForm(instance=hall)

        return render(request, self.template_name, {
            "hall_form": hall_form,
            "is_edit": True,
        })

    def post(self, request, pk):
        hall = self.get_object(pk)
        hall_form = HallForm(request.POST, instance=hall)

        if hall_form.is_valid():
            hall = hall_form.save()

            messages.success(request, "Hall updated successfully!")
            return redirect(self.success_url)

        # DEBUGGING
        # print("❌ Center form errors:", center_form.errors)
        # print("❌ Hall formset errors:", hall_formset.errors)
        # print("❌ Hall Images formset errors:", hall_images_formset.non_form_errors())
        # print("❌ Non-form errors:", hall_formset.non_form_errors())
        # Handle errors
        for field, errors in hall_form.errors.items():
            for error in errors:
                messages.error(request, f"{field.capitalize()}: {error}")

        return render(request, self.template_name, {
            "hall_form": hall_form,
            "is_edit": True,
        })


# Amenity List
class AmenityListView(ListView):
    model = Amenity
    template_name = "adminlte/amenity_list.html"
    context_object_name = "amenities"



# Amenity Create
class AmenityCreateView(SuccessMessageMixin, CreateView):
    model = Amenity
    template_name = "adminlte/amenity_form.html"
    success_url = reverse_lazy("services:amenity_list")
    form_class = AmenityForm
    success_message = "Amenity created successfully!"

# # Amenity Detail
class AmenityDetailView(DetailView):
    model = Amenity
    template_name = "adminlte/amenity_detail.html"
    context_object_name = "amenity"


# # Amenity Update
class AmenityUpdateView(SuccessMessageMixin, UpdateView):
    model = Amenity
    form_class = AmenityForm
    template_name = "adminlte/amenity_form.html"
    success_url = reverse_lazy("services:amenity_list")
    success_message = "Amenity updated successfully!"


# # Amenity Delete
class AmenityDeleteView(SuccessMessageMixin,DeleteView):
    model = Amenity
    template_name = "adminlte/amenity_confirm_delete.html"
    success_url = reverse_lazy("services:amenity_list")
    success_message = "Amenity deleted successfully!"



# class HallCreateView(View):
#     template_name = "adminlte/hall_form.html"
#     success_url = reverse_lazy("services:hall_list")
#
#     def get(self, request):
#         hall_form = HallForm()
#         rent_formset = HallRentFormSet(queryset=HallRent.objects.none())
#         hall_images_formset = HallImagesFormSet(queryset=HallImage.objects.none())
#         return render(request, self.template_name, {
#             "hall_form": hall_form,
#             "rent_formset": rent_formset,
#             "hall_images_formset": hall_images_formset,
#         })
#
#     def post(self, request):
#         hall_form = HallForm(request.POST)
#         rent_formset = HallRentFormSet(request.POST, queryset=HallRent.objects.none())
#         hall_images_formset = HallImagesFormSet(request.POST, request.FILES, queryset=HallImage.objects.none())
#         if hall_form.is_valid() and rent_formset.is_valid() and hall_images_formset.is_valid():
#             hall = hall_form.save()
#             rents = rent_formset.save(commit=False)
#             hall_images = hall_images_formset.save(commit=False)
#             for rent in rents:
#                 rent.hall = hall
#                 rent.save()
#
#             for hall_image in hall_images:
#                 hall_image.hall = hall
#                 hall_image.save()
#             return redirect(self.success_url)
#
#         return render(request, self.template_name, {
#             "hall_form": hall_form,
#             "rent_formset": rent_formset,
#             "hall_images_formset": hall_images_formset,
#         })


# class HallDeleteView(DeleteView):
#     model = Hall
#     template_name = "adminlte/hall_confirm_delete.html"
#     success_url = reverse_lazy("hall_list")
#
#
# class RentFormPartialView(View):
#     def get(self, request):
#         total_forms = int(request.GET.get("form-TOTAL_FORMS", 0))
#         rent_form = HallRentForm(prefix=f"form-{total_forms}")
#
#         # Update TOTAL_FORMS so Django knows about the new one
#         management_form = f'<input type="hidden" name="form-TOTAL_FORMS" id="id_form-TOTAL_FORMS" value="{total_forms + 1}">'
#
#         html = render_to_string("adminlte/rent_form.html", {"rent_form": rent_form})
#         return HttpResponse(management_form + html)
