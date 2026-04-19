import uuid
from django.db import models
from src.app.common.models import Basemodel
from django.utils.text import slugify

class TeamCategory(Basemodel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TeamMember(Basemodel):
    team = models.ForeignKey(
        TeamCategory,
        related_name="members",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)  # CEO & Founder
    bio = models.TextField()
    badge_name = models.CharField(max_length=50)  # Business Strategy, Innovation, etc.
    image_url = models.ImageField(upload_to="team/")

    def __str__(self):
        return self.name


class HeroImage(Basemodel):
    """Store hero images for the about page"""
    url = models.URLField(max_length=500)
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Hero Image {self.order}"


class AboutPage(Basemodel):
    """Store about page content"""
    title = models.CharField(max_length=255, default="About Choongshin")
    paragraphs = models.JSONField(default=list)  # Store as list of paragraph objects
    hero_images = models.ManyToManyField(HeroImage, related_name="about_pages")

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Pages"

    def __str__(self):
        return self.title


class JourneyMilestone(Basemodel):
    """Store journey milestones for the company timeline"""
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Journey Milestone"
        verbose_name_plural = "Journey Milestones"

    def __str__(self):
        return f"{self.year} - {self.title}"



