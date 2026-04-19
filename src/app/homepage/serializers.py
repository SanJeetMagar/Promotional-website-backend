from .models import LandingPage, HeroSection, HeroSectionImage
from rest_framework import serializers

class LandingPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage
        fields = ["id", "image_url", "caption","subtitle", "is_active", "order", ]

class HeroSectionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSectionImage
        fields = ["id", "image_url"]



class HeroSectionSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = HeroSection
        fields = [
            "id",
            "title",
            "description",
            "key_feature",
            "is_active",
            "order",
            "images",
        ]

    def get_images(self, obj):
        request = self.context.get("request")

        return [
            request.build_absolute_uri(image.image_url.url)
            if request else image.image_url.url
            for image in obj.images.all()
        ]



    
    