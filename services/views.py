from itertools import count

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Hall, HallRent, HallImage
from .forms import HallForm, HallRentForm, HallRentFormSet, HallImagesFormSet, HallImageForm


class HallListView(ListView):
    model = Hall
    template_name = "adminlte/hall_list.html"
    context_object_name = "halls"


# class HallCreateView(CreateView):
#     model = Hall
#     form_class = HallForm
#     template_name = "adminlte/hall_form.html"
#     success_url = reverse_lazy("hall_list")

class HallCreateView(View):
    template_name = "adminlte/hall_form.html"
    success_url = reverse_lazy("services:hall_list")

    def get(self, request):
        hall_form = HallForm()
        rent_formset = HallRentFormSet(queryset=HallRent.objects.none())
        hall_images_formset = HallImagesFormSet(queryset=HallImage.objects.none())
        return render(request, self.template_name, {
            "hall_form": hall_form,
            "rent_formset": rent_formset,
            "hall_images_formset": hall_images_formset,
        })

    def post(self, request):
        hall_form = HallForm(request.POST)
        rent_formset = HallRentFormSet(request.POST, queryset=HallRent.objects.none())
        hall_images_formset = HallImagesFormSet(request.POST, request.FILES, queryset=HallImage.objects.none())
        if hall_form.is_valid() and rent_formset.is_valid() and hall_images_formset.is_valid():
            hall = hall_form.save()
            rents = rent_formset.save(commit=False)
            hall_images = hall_images_formset.save(commit=False)
            for rent in rents:
                rent.hall = hall
                rent.save()

            for hall_image in hall_images:
                hall_image.hall = hall
                hall_image.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            "hall_form": hall_form,
            "rent_formset": rent_formset,
            "hall_images_formset": hall_images_formset,
        })




class HallUpdateView(UpdateView):
    model = Hall
    form_class = HallForm
    template_name = "adminlte/hall_form.html"
    success_url = reverse_lazy("hall_list")


class HallDeleteView(DeleteView):
    model = Hall
    template_name = "adminlte/hall_confirm_delete.html"
    success_url = reverse_lazy("hall_list")


class RentFormPartialView(View):
    def get(self, request):
        total_forms = int(request.GET.get("form-TOTAL_FORMS", 0))
        rent_form = HallRentForm(prefix=f"form-{total_forms}")

        # Update TOTAL_FORMS so Django knows about the new one
        management_form = f'<input type="hidden" name="form-TOTAL_FORMS" id="id_form-TOTAL_FORMS" value="{total_forms + 1}">'

        html = render_to_string("adminlte/rent_form.html", {"rent_form": rent_form})
        return HttpResponse(management_form + html)

class HallImagesFormPartialView(View):
    def get(self, request):
        total_forms = int(request.GET.get("form-TOTAL_FORMS", 0))  # match management form
        hall_images_form = HallImageForm(prefix=f"form-{total_forms}")

        # Update TOTAL_FORMS so Django knows about the new one
        management_form = (
            f'<input type="hidden" name="form-TOTAL_FORMS" id="id_form-TOTAL_FORMS" value="{total_forms + 1}">'
        )

        html = render_to_string("adminlte/hall_images_form.html", {"hall_image_form": hall_images_form})
        return HttpResponse(management_form + html)
