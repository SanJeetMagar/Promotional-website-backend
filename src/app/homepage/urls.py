from django.urls import path
from .views import LandingPageView, HeroSectionview


urlpatterns =[
        path('carousel/', LandingPageView.as_view(), name= "Carousel"),
        path('Hero-section/',HeroSectionview.as_view(),name="Hero-Section"),


]