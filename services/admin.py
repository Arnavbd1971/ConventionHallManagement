from django.contrib import admin
from .models import Center, CenterAdmin, Hall, HallImage, Amenity, HallAmenity


class CenterAdminInline(admin.TabularInline):
    model = CenterAdmin
    extra = 1
    fields = ("user", "role", "permissions")


class HallInline(admin.TabularInline):
    model = Hall
    extra = 1
    fields = ("name", "capacity", "price_currency", "price_per_hour", "price_per_day", "is_active")


@admin.register(Center)
class CenterAdminConfig(admin.ModelAdmin):
    list_display = ("name", "city", "district", "country", "status", "contact_phone", "created_at")
    search_fields = ("name", "city", "district", "country")
    list_filter = ("status", "city", "district", "country")
    inlines = [CenterAdminInline, HallInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(CenterAdmin)
class CenterAdminUserConfig(admin.ModelAdmin):
    list_display = ("center", "user", "role")
    search_fields = ("center__name", "user__username")
    list_filter = ("role",)


class HallImageInline(admin.TabularInline):
    model = HallImage
    extra = 1
    fields = ("image", "caption", "order")


class HallAmenityInline(admin.TabularInline):
    model = HallAmenity
    extra = 1
    fields = ("amenity",)


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("name", "center", "capacity", "price_currency", "is_active", "created_at")
    search_fields = ("name", "center__name")
    list_filter = ("is_active", "price_currency")
    inlines = [HallImageInline, HallAmenityInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(HallImage)
class HallImageAdmin(admin.ModelAdmin):
    list_display = ("hall", "caption", "order")
    search_fields = ("hall__name", "caption")


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(HallAmenity)
class HallAmenityAdmin(admin.ModelAdmin):
    list_display = ("hall", "amenity")
    search_fields = ("hall__name", "amenity__name")
