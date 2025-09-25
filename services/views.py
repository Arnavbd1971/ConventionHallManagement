from itertools import count

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Hall, HallRent
from .forms import HallForm, HallRentForm, HallRentFormSet


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
        return render(request, self.template_name, {
            "hall_form": hall_form,
            "rent_formset": rent_formset,
        })

    def post(self, request):
        hall_form = HallForm(request.POST)
        rent_formset = HallRentFormSet(request.POST, queryset=HallRent.objects.none())
        if hall_form.is_valid() and rent_formset.is_valid():
            hall = hall_form.save()
            rents = rent_formset.save(commit=False)
            for rent in rents:
                rent.hall = hall
                rent.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            "hall_form": hall_form,
            "rent_formset": rent_formset,
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