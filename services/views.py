from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Center, Hall, HallImage
from .forms import CenterForm
from .forms import (
                    CenterForm,
                    HallForm,
                    HallFormSet,
                    HallImagesFormSet,
                    HallImageForm
                    )

def dash_board_view(request):
    return render(request, "adminlte/dashboard.html", {})

class CenterListView(ListView):
    model = Center
    template_name = "adminlte/center_list.html"
    context_object_name = "centers"

    def get_queryset(self):
        return Center.objects.all().order_by('-id')

class CenterCreateView(View):
    template_name = "adminlte/center_form.html"
    success_url = reverse_lazy("services:center_list")

    def get(self, request):
        center_form = CenterForm()
        hall_formset = HallFormSet(queryset=Hall.objects.none())

        return render(request, self.template_name, {
            "center_form": center_form,
            "hall_formset": hall_formset,
        })

    def post(self, request):
        center_form = CenterForm(request.POST)
        hall_formset = HallFormSet(request.POST, queryset=Hall.objects.none())

        if center_form.is_valid() and hall_formset.is_valid():
            # Save Center first
            center = center_form.save()

            # Save each Hall and link to Center
            halls = hall_formset.save(commit=False)
            for hall in halls:
                hall.center = center
                hall.is_active = True
                hall.save()

            # Handle deleted halls (if can_delete=True)
            for hall in hall_formset.deleted_objects:
                hall.delete()

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

        return render(request, self.template_name, {
            "center_form": center_form,
            "hall_formset": hall_formset,
        })

class CenterDetailView(View):
    template_name = "adminlte/center_detail.html"

    def get(self, request, pk):
        center = Center.objects.get(pk=pk)
        hall_formset = HallFormSet(queryset=center.halls.all())

        return render(request, self.template_name, {
            "center": center,
            "hall_formset": hall_formset,
        })


class CenterUpdateView(View):
    template_name = "adminlte/center_form.html"
    success_url = reverse_lazy("services:center_list")

    def get_object(self, pk):
        return get_object_or_404(Center, pk=pk)

    def get(self, request, pk):
        center = self.get_object(pk)
        center_form = CenterForm(instance=center)
        hall_formset = HallFormSet(queryset=Hall.objects.filter(center=center))

        return render(request, self.template_name, {
            "center_form": center_form,
            "hall_formset": hall_formset,
            "is_edit": True,
        })

    def post(self, request, pk):
        center = self.get_object(pk)
        center_form = CenterForm(request.POST, instance=center)
        hall_formset = HallFormSet(request.POST, queryset=Hall.objects.filter(center=center))

        if center_form.is_valid() and hall_formset.is_valid():
            center = center_form.save()

            halls = hall_formset.save(commit=False)
            for hall in halls:
                hall.center = center
                hall.is_active = True
                hall.save()

            # Handle deleted halls
            for hall in hall_formset.deleted_objects:
                hall.delete()

            messages.success(request, "Center updated successfully!")
            return redirect(self.success_url)

        # DEBUGGING
        print("❌ Center form errors:", center_form.errors)
        print("❌ Hall formset errors:", hall_formset.errors)
        print("❌ Non-form errors:", hall_formset.non_form_errors())
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

        return render(request, self.template_name, {
            "center_form": center_form,
            "hall_formset": hall_formset,
            "is_edit": True,
        })


class HallFormPartialView(View):
    def get(self, request):
        total_forms = int(request.GET.get("form-TOTAL_FORMS", 0))
        hall_form = HallForm(prefix=f"form-{total_forms}")

        # Update TOTAL_FORMS so Django knows about the new one
        management_form = f'<input type="hidden" name="form-TOTAL_FORMS" id="id_form-TOTAL_FORMS" value="{total_forms + 1}">'

        html = render_to_string("adminlte/hall_form_inline.html", {"hall_form": hall_form})
        return HttpResponse(management_form + html)


class HallListView(ListView):
    model = Hall
    template_name = "adminlte/hall_list.html"
    context_object_name = "halls"

    def get_queryset(self):
        return Hall.objects.filter(is_active=True).order_by('-id')


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
#
# class HallDetailView(View):
#     template_name = "adminlte/hall_detail.html"
#
#     def get(self, request, pk):
#         hall = Hall.objects.get(pk=pk)
#         rent_formset = HallRentFormSet(queryset=hall.rents.all())   # rents linked to hall
#         hall_images_formset = HallImagesFormSet(queryset=hall.images.all())  # images linked to hall
#
#         return render(request, self.template_name, {
#             "hall": hall,
#             "rent_formset": rent_formset,
#             "hall_images_formset": hall_images_formset,
#         })
#
#
#
# class HallUpdateView(UpdateView):
#     model = Hall
#     form_class = HallForm
#     template_name = "adminlte/hall_form.html"
#     success_url = reverse_lazy("hall_list")
#
#
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
#
# class HallImagesFormPartialView(View):
#     def get(self, request):
#         total_forms = int(request.GET.get("form-TOTAL_FORMS", 0))  # match management form
#         hall_images_form = HallImageForm(prefix=f"form-{total_forms}")
#
#         # Update TOTAL_FORMS so Django knows about the new one
#         management_form = (
#             f'<input type="hidden" name="form-TOTAL_FORMS" id="id_form-TOTAL_FORMS" value="{total_forms + 1}">'
#         )
#
#         html = render_to_string("adminlte/hall_images_form.html", {"hall_image_form": hall_images_form})
#         return HttpResponse(management_form + html)
