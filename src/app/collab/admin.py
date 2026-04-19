from django.contrib import admin
from .models import CollabCompany

@admin.register(CollabCompany)
class CollabCompanyAdmin(admin.ModelAdmin):
    list_display = ["title"]