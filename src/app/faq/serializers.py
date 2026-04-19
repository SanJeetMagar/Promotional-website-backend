from .models import faq
from rest_framework import serializers


class FAQSerializer(serializers.ModelSerializer):  
    class Meta:
        model = faq
        fields = '__all__'