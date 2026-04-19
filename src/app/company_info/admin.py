from django.contrib import admin
from .models import TeamMember, TeamCategory, HeroImage, AboutPage, JourneyMilestone

@admin.register(TeamCategory)
class TeamCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug")
    readonly_fields = ("slug",)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "team", "position")
    list_filter = ("team",)
    search_fields = ("name", "position")

@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "alt_text", "url")
    list_editable = ("order",)
    search_fields = ("alt_text", "url")
    ordering = ("order",)

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    filter_horizontal = ("hero_images",)
    
    fieldsets = (
        ("Basic Info", {
            "fields": ("title",)
        }),
        ("Content", {
            "fields": ("paragraphs",),
            "description": "Enter paragraphs as a JSON array. Example: [{\"text\": \"Your paragraph here\", \"highlight\": false}]"
        }),
        ("Hero Images", {
            "fields": ("hero_images",)
        }),
    )

@admin.register(JourneyMilestone)
class JourneyMilestoneAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "year", "title")
    list_editable = ("order",)
    search_fields = ("year", "title", "description")
    ordering = ("order",)
