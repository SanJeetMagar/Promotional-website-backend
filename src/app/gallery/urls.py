from django.urls import path
from .views import GalleryImageListAPIView, PosterListView

urlpatterns = [
    path("gallery/", GalleryImageListAPIView.as_view(), name="gallery-list"),
    path("poster/",PosterListView.as_view(), name="poster")
]
