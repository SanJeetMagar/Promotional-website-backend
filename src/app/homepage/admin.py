from django.contrib import admin
from django.utils.html import format_html
from .models import LandingPage, HeroSection, HeroSectionImage


@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "caption","subtitle", "is_active", "thumbnail")
    list_editable = ("order", "is_active")
    search_fields = ("caption",)
    list_filter = ("is_active",)
    ordering = ("order",)
    readonly_fields = ("created_at", "updated_at", "large_preview")

    fieldsets = (
        ("Details", {
            "fields": ("caption","subtitle", "order", "is_active")
        }),
        ("Image", {
            "fields": ("image_url", "large_preview"),
        }),
        ("System Info", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )

    # Small preview inside list view
    def thumbnail(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" width="60" style="border-radius:6px;" />',
                obj.image_url.url
            )
        return "No Image"

    thumbnail.short_description = "Preview"

    # Large preview inside edit form
    def large_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" width="300" style="border-radius:8px;" />',
                obj.image_url.url
            )
        return "No Image"

    large_preview.short_description = "Large Preview"


class HeroSectionImageInline(admin.TabularInline):
    model = HeroSectionImage
    extra = 1
    fields = ["image_url"]

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title","is_active","order","key_feature")
    inlines =[HeroSectionImageInline]