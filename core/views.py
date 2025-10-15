from django.contrib import messages
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View

from core.forms import CustomUserCreationForm, SliderImageForm, WebsiteConfigurationForm, SliderFormSet
from core.models import CUser, SliderImage, WebsiteConfiguration
from core.utils import send_verification_email
from services.models import Hall, Center
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


# @login_required
def home(request):
    web_config = WebsiteConfiguration.objects.first()
    sliders = SliderImage.objects.filter(is_active=True).order_by("id")
    centers = Center.objects.filter(status="approved").order_by("-id")
    return render(request, "home.html", {
        "centers": centers,
        "web_config": web_config,
        "sliders": sliders,
    })

def hallDetail(request, pk):
    hall = get_object_or_404(Hall, pk=pk)
    hall_images = hall.images.all()
    hall_rents = hall.rents.all()

    return render(request, "hall_details.html", {
        "hall": hall,
        "hall_images": hall_images,
        "hall_rents": hall_rents,
    })


def customerSignupView(request):
    """Signup view for customers"""
    return _handle_signup(request, user_type="customer")


def centerOwnerSignupView(request):
    """Signup view for center owners"""
    return _handle_signup(request, user_type="center_owner")


def _handle_signup(request, user_type):
    """Shared signup handler for both types"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.type = user_type
            user.is_active = False  # user inactive until verified
            user.save()

            # Send email verification link and code
            send_verification_email(user, request)

            messages.success(
                request,
                "Account created! Please check your email for the verification link or code."
            )
            return redirect("core:verify_email")
        else:
            print(form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form, "user_type": user_type})


def verify_email(request):
    """Handle both link-based and code-based email verification"""

    # Case A: User clicked link with token
    token = request.GET.get("token")
    if token:
        try:
            user = CUser.objects.get(verification_token=token)
        except CUser.DoesNotExist:
            messages.error(request, "Invalid or expired verification link.")
            return redirect("core:verify_email")

        # Optional expiry check
        if user.verification_sent_at and timezone.now() - user.verification_sent_at > timedelta(minutes=10):
            messages.error(request, "Verification link expired. Please sign up again.")
            return redirect("core:verify_email")

        # Activate the account
        user.is_active = True
        user.is_email_verified = True
        user.save(update_fields=["is_active", "is_email_verified"])
        messages.success(request, "Your email has been verified successfully! You can now log in.")
        return redirect("core:login")

    # Case B: User manually entered code
    if request.method == "POST":
        email = request.POST.get("email")
        code = request.POST.get("code")

        try:
            user = CUser.objects.get(email=email)
        except CUser.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect("core:verify_email")

        # Check expiry
        if user.verification_sent_at and timezone.now() - user.verification_sent_at > timedelta(minutes=10):
            messages.error(request, "Verification code expired. Please sign up again.")
            return redirect("core:verify_email")

        if user.verification_code == code:
            user.is_active = True
            user.is_email_verified = True
            user.save(update_fields=["is_active", "is_email_verified"])
            messages.success(request, "Your email has been verified successfully! You can now log in.")
            return redirect("core:login")
        else:
            messages.error(request, "Invalid verification code.")
            return redirect("core:verify_email")

    return render(request, "registration/verify_email.html")


# work for web confiq
class WebConfigurationView(View):
    template_name = "adminlte/webconfig_form.html"
    success_url = reverse_lazy("core:webconfig")

    def get(self, request):
        config, _ = WebsiteConfiguration.objects.get_or_create(id=1)
        config_form = WebsiteConfigurationForm(instance=config)
        slider_formset = SliderFormSet(
            queryset=SliderImage.objects.filter(website=config),
            prefix="sliderimage"
        )
        return render(request, self.template_name, {
            "config_form": config_form,
            "slider_images_formset": slider_formset,
        })

    def post(self, request):
        config, _ = WebsiteConfiguration.objects.get_or_create(id=1)
        config_form = WebsiteConfigurationForm(request.POST, request.FILES, instance=config)
        slider_formset = SliderFormSet(
            request.POST, request.FILES,
            queryset=SliderImage.objects.filter(website=config),
            prefix="sliderimage"
        )

        if config_form.is_valid() and slider_formset.is_valid():
            config = config_form.save()
            sliders = slider_formset.save(commit=False)

            for slider in sliders:
                slider.website = config
                slider.is_active = True
                slider.save()

            for deleted in slider_formset.deleted_objects:
                deleted.delete()

            messages.success(request, "✅ Website configuration updated successfully!")
            return redirect(self.success_url)

        # --- Collect specific error messages ---
        error_messages = []

        if not config_form.is_valid():
            for field, errors in config_form.errors.items():
                for e in errors:
                    error_messages.append(f"General field '{field}': {e}")

        if not slider_formset.is_valid():
            for i, form in enumerate(slider_formset.forms):
                if not form.is_valid():
                    # skip deleted forms
                    if form.cleaned_data.get("DELETE", False):
                        continue
                    for field, errors in form.errors.items():
                        for e in errors:
                            error_messages.append(f"Slider #{i + 1} - {field}: {e}")

            # also check non-formset errors (like management form tampering)
            for e in slider_formset.non_form_errors():
                error_messages.append(str(e))

        # Display detailed error summary
        if error_messages:
            for msg_text in error_messages:
                messages.error(request, msg_text)
        else:
            messages.error(request, "Please fix the errors below.")

        return render(request, self.template_name, {
            "config_form": config_form,
            "slider_images_formset": slider_formset,
        })


class SliderImagesFormPartialView(View):
    def get(self, request):
        total_forms = int(request.GET.get("sliderimage-TOTAL_FORMS", 0))
        form = SliderImageForm(prefix=f"sliderimage-{total_forms}")
        management_form = (
            f'<input type="hidden" name="sliderimage-TOTAL_FORMS" id="id_sliderimage-TOTAL_FORMS" value="{total_forms + 1}">'
        )
        html = render_to_string("adminlte/slider_images_form.html", {"slider_image_form": form})
        return HttpResponse(management_form + html)
