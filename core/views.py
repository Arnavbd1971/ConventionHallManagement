from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from core.forms import CustomUserCreationForm
from services.models import Hall


# @login_required
def home(request):
    halls = Hall.objects.all().order_by("-id")[:6]
    return render(request, "home.html", {"halls": halls})

def hallDetail(request, pk):
    hall = get_object_or_404(Hall, pk=pk)
    hall_images = hall.images.all()
    hall_rents = hall.rents.all()

    return render(request, "hall_details.html", {
        "hall": hall,
        "hall_images": hall_images,
        "hall_rents": hall_rents,
    })



def authView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("core:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
