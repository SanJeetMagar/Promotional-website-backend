from .models import LandingPage, HeroSection
from .serializers import LandingPagesSerializer, HeroSectionSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["HomePage"])
class LandingPageView(generics.ListAPIView):
    queryset = LandingPage.objects.filter(is_active=True).order_by('order')
    serializer_class = LandingPagesSerializer
    pagination_class = None


@extend_schema(tags=["HomePage"])
class HeroSectionview(generics.ListAPIView):
    queryset = HeroSection.objects.filter(is_active =True).order_by("order")
    serializer_class = HeroSectionSerializer
    pagination_class = None