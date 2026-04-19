from django.db import models
from src.app.common.models import Basemodel

class LandingPage(Basemodel):
    caption = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    order =  models.IntegerField(default=0, help_text="Images order in slideshow ")
    image_url = models.ImageField(upload_to="landing-page/")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
    
    def __str__(self) -> str:
        return f"{self.order} - {self.caption}"



class HeroSection(Basemodel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    key_feature = models.TextField()
    is_active = models.BooleanField(default= True)
    # image_url = models.ImageField(upload_to="vertical-image")
    order = models.IntegerField(default=0, help_text="Image order")
    def __str__(self) -> str:
        return self.title
    

class HeroSectionImage(Basemodel):
    hero = models.ForeignKey(
        HeroSection,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image_url = models.ImageField(upload_to="hero-gallery")

    def __str__(self):
        return f"Image for {self.hero.title}"
