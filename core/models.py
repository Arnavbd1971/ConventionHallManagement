import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
import random

class CUser(AbstractUser):
    type = models.CharField(
        max_length=20,
        choices=[("customer", "Customer"), ("center_owner", "Center-Owner"), ("admin_user", "Admin-User")]
    )
    email = models.EmailField(unique=True, null=False, blank=False, validators=[validate_email])
    phone = models.CharField(max_length=20, unique=True, null=False, blank=False, default='+8801')
    is_social_login = models.BooleanField(default=False)

    # Email verification fields
    is_email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_sent_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.is_social_login and not self.password:
            raise ValueError("Password is required for non-social logins.")
        super().save(*args, **kwargs)

    def generate_verification_token(self):
        """Generate a unique token and 6-digit verification code."""
        self.verification_token = str(uuid.uuid4())
        self.verification_code = str(random.randint(100000, 999999))
        self.verification_sent_at = timezone.now()
        self.save(update_fields=["verification_token", "verification_code", "verification_sent_at"])

class WebsiteConfiguration(models.Model):
    site_name = models.CharField(max_length=150, default="My Website")
    logo = models.ImageField(upload_to="website/logo/", null=True, blank=True)
    logo_size = models.CharField(max_length=150, default="50")
    about_us = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name


class SliderImage(models.Model):
    website = models.ForeignKey(
        WebsiteConfiguration,
        related_name="sliders",
        on_delete=models.CASCADE,
        default=1
    )
    image = models.ImageField(upload_to="website/sliders/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    caption_sub = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Auto-assign order if not set
        if self.order is None:
            last_order = SliderImage.objects.filter(website=self.website).aggregate(models.Max('order'))['order__max'] or 0
            self.order = last_order + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.caption or f"Slider {self.id}"

class EventType(models.Model):
    event_name = models.CharField(max_length=150, default="Marriage")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name
