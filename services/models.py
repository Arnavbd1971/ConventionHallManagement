from django.db import models

class Hall(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.PositiveIntegerField(help_text="Maximum number of persons")
    batch = models.PositiveIntegerField(help_text="Maximum number of persons can dine",default=0)
    area_size = models.CharField(max_length=50, blank=True, null=True)
    parking_capacity = models.PositiveIntegerField(blank=True, null=True)
    year_built = models.DateField(blank=True, null=True)
    is_government_property = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class HallShift(models.TextChoices):
    DAY = "day", "Day Shift"
    NIGHT = "night", "Night Shift"
    FULL = "full", "Day & Night Shift"


class Season(models.TextChoices):
    NOV_JAN = "nov_jan", "November – January"
    FEB_OCT = "feb_oct", "February – October"


class HallRent(models.Model):
    hall = models.ForeignKey(Hall, related_name="rents", on_delete=models.CASCADE)
    season = models.CharField(max_length=20, choices=Season.choices)
    shift = models.CharField(max_length=20, choices=HallShift.choices)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ("hall", "season", "shift")

    def __str__(self):
        return f"{self.hall.name} - {self.get_season_display()} - {self.get_shift_display()}"


class HallImage(models.Model):
    hall = models.ForeignKey(Hall, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="hall_images/")
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image of {self.hall.name}"
