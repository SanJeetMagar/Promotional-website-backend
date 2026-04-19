from django.db import models
from src.app.common.models import Basemodel
# from django.contrib.postgres.fields import ArrayField


class Contact(Basemodel):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20,blank=True)
    subject = models.CharField(max_length=100)
    message =models.TextField(max_length=255)

    def __str__(self) -> str:
        return f"{self.full_name} - {self.subject}"

class Newsletter(Basemodel):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class Company_info(Basemodel):
    mail = models.EmailField()
    address = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    business_hour = models.CharField(max_length=255)
    tiktok = models.URLField(blank=True, max_length=255)
    whatsapp = models.URLField(blank=True, max_length=255)
    facebook = models.URLField(blank=True, max_length=255)
    instagram = models.URLField(blank=True, max_length=255)

    def __str__(self):
        return "Company Info"
    

class Tagline(Basemodel):
    company = models.ForeignKey(
        Company_info,
        on_delete=models.CASCADE,
        related_name="taglines"
    )
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
