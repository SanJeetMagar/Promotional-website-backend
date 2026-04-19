from django.db import models
from src.app.common.models import Basemodel
class GalleryImage(Basemodel):
    title = models.CharField(max_length=255, blank=True, null= True)
    image_url = models.ImageField(upload_to="gallery/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Poster(Basemodel):
    title = models.CharField(max_length=255)
    image_url = models.ImageField(upload_to="posters/")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
    def __str__(self) -> str:
        return self.title
    

    