from django.db import models
from src.app.common.models import Basemodel

class CollabCompany(Basemodel):
    title = models.CharField(max_length=255)
    image_url =models.ImageField(upload_to="collab-logo/")
    def __str__(self) -> str:
        return self.title

