from django.db import models
from django.conf import settings
from django.utils import timezone

import core.models
from services.models import Center, Hall

from django.core.exceptions import ValidationError



# -------------------------
# Booking
# -------------------------
class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
        ("rejected", "Rejected"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("paid", "Paid"),
        ("refunded", "Refunded"),
        ("partial", "Partial"),
    ]

    SHIFT = [
        ("day", "Day"),
        ("night", "Night"),
        ("day_and_night", "Full Day")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings_user")
    name = models.CharField(max_length=100, default="")
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True, default="example@mail.com")
    phone = models.CharField(max_length=20, default="")
    event_type = models.ForeignKey(core.models.EventType, on_delete=models.CASCADE, related_name="booking_event_type", default=1)
    number_of_guest = models.IntegerField(blank=True, null=True)
    shift = models.CharField(max_length=20, choices=SHIFT, default="day_and_night")

    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name="bookings_center")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="bookings_hall")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    duration_minutes = models.IntegerField(blank=True, null=True, editable=False)

    special_requests = models.TextField(blank=True, null=True)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default="BDT")

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="unpaid")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        """Prevent overlapping bookings for the same hall."""
        if self.start_datetime >= self.end_datetime:
            raise ValidationError("End time must be after start time.")

        overlapping = Booking.objects.filter(
            hall=self.hall,
            start_datetime__lte=self.end_datetime,   # starts before this one ends
            end_datetime__gte=self.start_datetime    # ends after this one starts
        )

        # Exclude itself if updating
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("This booking overlaps with an existing one.")

    def save(self, *args, **kwargs):
        # Run validation automatically
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.hall.name} booked from {self.start_datetime} to {self.end_datetime}"


# -------------------------
# Payment
# -------------------------
class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("refunded", "Refunded"),
        ("failed", "Failed"),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments_booking")
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    transaction_at = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"Payment ({self.status})"


# -------------------------
# Commission
# -------------------------
class Commission(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="commission_booking")

    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    platform_commission_amount = models.DecimalField(max_digits=12, decimal_places=2)
    partner_share_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    center_amount = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Commission for {self.booking.id}"
