from .models import faq
from .serializers import FAQSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["FAQ"])
class FaqView(generics.ListAPIView):
    queryset = faq.objects.all()
    serializer_class = FAQSerializer
    pagination_class = None
