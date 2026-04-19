from rest_framework import serializers
from .models import CollabCompany
 

class CollabCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model =CollabCompany
        fields = [
            "id",
            "title",
            "image_url"
        ]