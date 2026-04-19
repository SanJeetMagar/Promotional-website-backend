from django.urls import path
from .views import (
    MegaMenuView,
    ProductListView,
    ProductDetailView,
    FeaturedProductListView,
    CategoryListView,
    PopularProductListView,
    
    OccasionListView,
    ProductsByOccasionView,
    
    RecipientListView,
    RecipientDetailView,
    ProductsByRecipientView,
)

app_name = "products"

urlpatterns = [
    path("products/menu/", MegaMenuView.as_view()),
    path("products/categories/", CategoryListView.as_view()),
    path("products/", ProductListView.as_view()),
    path("products/featured/", FeaturedProductListView.as_view()),
    path("products/popular/", PopularProductListView.as_view()),
    path("products/<slug:slug>/", ProductDetailView.as_view()),
    path("occasions/", OccasionListView.as_view()),
    path("occasions/<slug:slug>/products/", ProductsByOccasionView.as_view()),
    path("recipients/", RecipientListView.as_view()),
    path("recipients/<slug:slug>/", RecipientDetailView.as_view()),
    path("recipients/<slug:slug>/products/", ProductsByRecipientView.as_view()),
]