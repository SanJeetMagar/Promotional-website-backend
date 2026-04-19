# gallery/admin.py
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django import forms
from .widgets import MultipleFileInput
from .models import GalleryImage, Poster
class GalleryImageUploadForm(forms.ModelForm):
    image_url = forms.ImageField(
        widget=MultipleFileInput(),
        label="Upload Images"
    )

    class Meta:
        model = GalleryImage
        fields = ("title", "image_url")

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    form = GalleryImageUploadForm
    list_display = ("id", "title", "created_at")

    def add_view(self, request, form_url="", extra_context=None):
        if request.method == "POST":
            files = request.FILES.getlist("image_url")
            base_title = request.POST.get("title", "")

            for file in files:
                # Use your manually typed title instead of filename
                GalleryImage.objects.create(
                    title=base_title,
                    image_url=file
                )

            self.message_user(request, f"{len(files)} images uploaded successfully.")
            return HttpResponseRedirect("../")

        return super().add_view(request, form_url, extra_context)

@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "thumbnail", "is_active", "order")
    list_editable = ("is_active", "order")
    search_fields = ("title",)

    fieldsets = (
        ("Poster Details", {
            "fields": ("title", "image_url", "preview")
        }),
        ("Settings", {
            "fields": ("order", "is_active")
        }),
    )

    readonly_fields = ("preview",)

    def thumbnail(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" width="70" style="border-radius:6px"/>',
                obj.image_url.url,
            )
        return "No Image"

    def preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" width="200" style="border-radius:6px"/>',
                obj.image_url.url,
            )
        return "No Image"
