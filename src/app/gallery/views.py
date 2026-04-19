from rest_framework import generics
from .models import GalleryImage, Poster 
from .serializers import GalleryImageSerializer, PosterSerializer
# from .pagination import CustomGalleryPagination
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Gallery"])
class GalleryImageListAPIView(generics.ListAPIView):
    queryset = GalleryImage.objects.all().order_by("-id")
    serializer_class = GalleryImageSerializer
    # pagination_class = CustomGalleryPagination
 
@extend_schema(tags =["Poster"])
class PosterListView(generics.ListAPIView):
    queryset = Poster.objects.filter(is_active=True)
    serializer_class = PosterSerializer