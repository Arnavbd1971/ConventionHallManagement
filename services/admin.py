from django.contrib import admin
from .models import Center, CenterAdmin, Hall, HallImage, Amenity


class CenterAdminInline(admin.TabularInline):
    model = CenterAdmin
    extra = 1
    fields = ("user", "role", "permissions")


class HallInline(admin.TabularInline):
    model = Hall
    extra = 1
    fields = ("name", "capacity", "price_currency", "price_per_hour", "price_per_day", "is_active")

class HallImageInline(admin.TabularInline):
    model = HallImage
    extra = 1
    fields = ("image", "caption", "order")


@admin.register(Center)
class CenterAdminConfig(admin.ModelAdmin):
    list_display = ("name", "city", "district", "country", "status", "contact_phone", "created_at")
    search_fields = ("name", "city", "district", "country")
    list_filter = ("status", "city", "district", "country")
    inlines = [CenterAdminInline, HallInline, HallImageInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(CenterAdmin)
class CenterAdminUserConfig(admin.ModelAdmin):
    list_display = ("center", "user", "role")
    search_fields = ("center__name", "user__username")
    list_filter = ("role",)


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("name", "center", "capacity", "price_currency", "is_active", "created_at")
    search_fields = ("name", "center__name")
    list_filter = ("is_active", "price_currency")
    inlines = []
    readonly_fields = ("created_at", "updated_at")


@admin.register(HallImage)
class HallImageAdmin(admin.ModelAdmin):
    list_display = ("center", "caption", "order")
    search_fields = ("center__name", "caption")


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


