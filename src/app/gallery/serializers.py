from rest_framework import serializers
from .models import GalleryImage, Poster

class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ["id","title", "image_url"]
class PosterSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Poster
        fields = ["id", "title", "image_url", "order"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image_url and request:
            return request.build_absolute_uri(obj.image_url.url)
        return None
