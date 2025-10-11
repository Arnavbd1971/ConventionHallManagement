from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from core.forms import CustomUserCreationForm
from core.models import CUser
from core.utils import send_verification_email
from services.models import Hall
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


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

    # 1️⃣ Case A: User clicked link with token
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

