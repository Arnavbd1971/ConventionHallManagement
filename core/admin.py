from django.contrib import admin

from core.models import CUser, WebsiteConfiguration, SliderImage

admin.site.register(CUser)



class SliderImageInline(admin.TabularInline):
    model = SliderImage
    extra = 1
    fields = ('image', 'caption', 'caption_sub', 'order', 'is_active')
    readonly_fields = ()
    show_change_link = True


@admin.register(WebsiteConfiguration)
class WebsiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'updated_at')
    inlines = [SliderImageInline]
    search_fields = ('site_name',)
    readonly_fields = ('updated_at',)


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'caption_sub', 'order', 'is_active', 'website')
