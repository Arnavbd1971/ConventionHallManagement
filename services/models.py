import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.utils import timezone

User = get_user_model()

# -------------------------
# Center Model
# -------------------------
class Center(models.Model):
    owner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=255) #unique=True
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True) #unique=True
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True) #unique=True
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True) #unique=True
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True, default="Bangladesh")
    amenities = models.ManyToManyField("services.Amenity", related_name="centers", blank=True)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("suspended", "Suspended"),
        ("deleted", "Deleted"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# -------------------------
# Center Admins
# -------------------------
class CenterAdmin(models.Model):
    ROLE_CHOICES = [
        ("manager", "Manager"),
        ("staff", "Staff"),
    ]

    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name="admins",default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="center_roles")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    permissions = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.role} @ {self.center}"


# -------------------------
# Halls
# -------------------------
class Hall(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name="halls",default=1)
    name = models.TextField(max_length=255) #unique=True
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    price_currency = models.CharField(max_length=10, default="BDT")
    price_per_hour = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    min_booking_hours = models.PositiveIntegerField(default=1)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True) #unique=True
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True) #unique=True
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# -------------------------
# Hall Images
# -------------------------
class HallImage(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name="center_images", default=1)
    image = models.ImageField(upload_to="hall_images/")
    caption = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.center.name}"


# -------------------------
# Amenities
# -------------------------
class Amenity(models.Model):
    name = models.TextField(unique=True)
    icon = models.ImageField(upload_to="hall_images/", default="hall_images/default_icon.png",)

    def __str__(self):
        return self.name




