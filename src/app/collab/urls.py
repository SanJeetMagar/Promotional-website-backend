from django.urls import path
from .views import CollabCompanyView

urlpatterns =[
    path("",CollabCompanyView.as_view(), name="collab"),
]