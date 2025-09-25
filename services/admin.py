from django.contrib import admin
from .models import Hall, HallRent, HallImage


class HallRentInline(admin.TabularInline):  # or admin.StackedInline
    model = HallRent
    extra = 1   # how many empty forms to show
    fields = ("season", "shift", "price")


class HallImageInline(admin.TabularInline):
    model = HallImage
    extra = 1
    fields = ("image", "caption")


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "location", "parking_capacity", "updated_on")
    search_fields = ("name", "location")
    list_filter = ("is_government_property", "year_built")
    inlines = [HallRentInline, HallImageInline]


@admin.register(HallRent)
class HallRentAdmin(admin.ModelAdmin):
    list_display = ("hall", "season", "shift", "price")
    list_filter = ("season", "shift")
    search_fields = ("hall__name",)


@admin.register(HallImage)
class HallImageAdmin(admin.ModelAdmin):
    list_display = ("hall", "caption")
    search_fields = ("hall__name", "caption")
