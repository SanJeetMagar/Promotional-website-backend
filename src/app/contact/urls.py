from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, NewsletterViewSet, ContactDetailView
from django.urls import path

router = DefaultRouter()
router.register("contact", ContactViewSet, basename="contact")
router.register("newsletter", NewsletterViewSet, basename="newsletter")

urlpatterns = [
    path("company-info/",ContactDetailView.as_view(), name="social-info")
]

urlpatterns += router.urls
