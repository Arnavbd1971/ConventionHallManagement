from django.db import models
from django.contrib.auth.models import AbstractUser

class CUser(AbstractUser):
    type = models.CharField(
        max_length=20,
        choices=[("member", "Member"), ("organizer", "Organizer"), ("admin", "Admin")]
    )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
