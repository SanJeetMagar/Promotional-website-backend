from .models import CollabCompany
from .serializers import CollabCompanySerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Collabator"])
class CollabCompanyView(generics.ListAPIView):
    queryset = CollabCompany.objects.all()
    serializer_class = CollabCompanySerializer
    pagination_class = None