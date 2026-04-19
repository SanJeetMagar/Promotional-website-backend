from django.contrib import admin
from .models import faq


@admin.register(faq)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'created_at']
    search_fields = ['question', 'answer']
