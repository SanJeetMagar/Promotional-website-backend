from django.db import models
from django.db.models import Q, OuterRef, Subquery, Count, F

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import (
    Product,
    ProductImage,
    MainCategory,
    Category,
    Occasion,
    Recipient, 
)
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    MegaMenuSerializer,
    NestedCategorySerializer,
    OccasionSerializer,
    RecipientSerializer,  
)
from .pagination import ProductPagination

@extend_schema(tags=["Product"])
class MegaMenuView(APIView):
    """Returns main categories with nested categories for mega menu"""
    def get(self, request):
        queryset = (
            MainCategory.objects
            .prefetch_related(
                "categories",
                "categories__products",
                "categories__products__images",
            )
        )
        serializer = MegaMenuSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


@extend_schema(
    tags=["Product"],
    parameters=[
        OpenApiParameter("main", OpenApiTypes.STR, description="Main category slug (optional)")
    ]
)
class CategoryListView(ListAPIView):
    """List all categories, optionally filtered by main category"""
    serializer_class = NestedCategorySerializer

    def get_queryset(self):
        queryset = Category.objects.select_related("categorygroup")

        main_slug = self.request.query_params.get("main")
        if main_slug:
            queryset = queryset.filter(categorygroup__slug=main_slug)

        return queryset.order_by("name")


@extend_schema(
    tags=["Product"],
    parameters=[
        OpenApiParameter("page", OpenApiTypes.INT),
        OpenApiParameter("limit", OpenApiTypes.INT),
        OpenApiParameter("search", OpenApiTypes.STR),
        OpenApiParameter("categories", OpenApiTypes.STR, description="Category slugs (comma-separated)"),
        OpenApiParameter("maincategories", OpenApiTypes.STR, description="Main category slugs (comma-separated)"),
        OpenApiParameter("sort_by", OpenApiTypes.STR, description="name.asc, name.desc, created_at.asc, created_at.desc"),
        OpenApiParameter("popular", OpenApiTypes.BOOL),
        OpenApiParameter("featured", OpenApiTypes.BOOL),
    ]
)
class ProductListView(ListAPIView):
    """List products with filtering, search, and sorting"""
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        params = self.request.query_params

        # SEARCH
        search = params.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(slug__icontains=search) |
                Q(category__name__icontains=search)
            ).distinct()

        # CATEGORY FILTER
        categories = params.get("categories")
        if categories:
            slugs = [s.strip() for s in categories.split(",") if s.strip()]
            queryset = queryset.filter(category__slug__in=slugs).distinct()

        # MAIN CATEGORY FILTER
        maincats = params.get("maincategories")
        if maincats:
            slugs = [s.strip() for s in maincats.split(",") if s.strip()]
            queryset = queryset.filter(
                category__categorygroup__slug__in=slugs
            ).distinct()

        # FEATURED
        if params.get("featured", "").lower() == "true":
            queryset = queryset.filter(is_featured=True)

        # POPULAR
        if params.get("popular", "").lower() == "true":
            queryset = queryset.filter(is_popular=True)
        sort_by = params.get("sort_by") 
        sort_map = {
            "name.asc": "name",
            "name.desc": "-name",
            "created_at.asc": "created_at",
            "created_at.desc": "-created_at",
        }

        queryset = queryset.order_by(sort_map.get(sort_by, "-created_at"))

        return queryset.prefetch_related("category", "images", "tags") 


@extend_schema(tags=["Product"])
class ProductDetailView(RetrieveAPIView):
    """Get single product with similar products"""
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .prefetch_related(
                "category",
                "tags",
                "occasions",
                "recipients",
                "images",
                "specifications",
                "keyfeatures",
            )
        )

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        similar_products = (
            Product.objects.filter(is_active=True)
            .exclude(id=product.id)
            .annotate(
                same_category=Count(
                    "category",
                    filter=Q(category__in=product.category.all()),
                    distinct=True,
                ),
                same_tags=Count(
                    "tags",
                    filter=Q(tags__in=product.tags.all()),
                    distinct=True,
                ),
                same_occasions=Count(
                    "occasions",
                    filter=Q(occasions__in=product.occasions.all()),
                    distinct=True,
                ),
            )
            .annotate(
                relevance=(
                    3 * F("same_category")
                    + 4 * F("same_tags")
                    + 2 * F("same_occasions")
                )
            )
            .filter(relevance__gt=0)
            .prefetch_related("category", "images", "tags")
            .order_by("-relevance", "-created_at")
            .distinct()[:8]
        )

        if not similar_products.exists():
            similar_products = (
                Product.objects.filter(
                    category__in=product.category.all(),
                    is_active=True,
                )
                .exclude(id=product.id)
                .distinct()[:8]
            )

        data = self.get_serializer(product).data
        data["similar_products"] = ProductListSerializer(
            similar_products,
            many=True,
            context={"request": request},
        ).data

        return Response(data)


@extend_schema(tags=["Product"])
class FeaturedProductListView(ListAPIView):
    """List featured products"""
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True, is_featured=True)
            .prefetch_related("category", "images", "tags")
            .order_by("-created_at")
            .distinct()
        )


@extend_schema(tags=["Product"])
class PopularProductListView(ListAPIView):
    """List popular products"""
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True, is_popular=True)
            .prefetch_related("category", "images", "tags")
            .order_by("-created_at")
            .distinct()
        )

@extend_schema(tags=["Occasion"])
class OccasionListView(ListAPIView):
    """
    List all active occasions (Father's Day, Dashain, etc.)
    Returns occasions ordered by display_order
    """
    serializer_class = OccasionSerializer

    def get_queryset(self):
        return Occasion.objects.filter(is_active=True).order_by('display_order', 'title')


@extend_schema(
    tags=["Occasion"],
    parameters=[
        OpenApiParameter("page", OpenApiTypes.INT),
        OpenApiParameter("sort_by", OpenApiTypes.STR, description="name.asc, name.desc, created_at.asc, created_at.desc"),
    ]
)
class ProductsByOccasionView(ListAPIView):
    """
    Get all products for a specific occasion with pagination
    Example: /occasions/fathers-day/products/
    """
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        slug = self.kwargs["slug"]
        params = self.request.query_params

        queryset = (
            Product.objects
            .filter(occasions__slug=slug, is_active=True)
            .prefetch_related(
                "category",
                "category__categorygroup",
                "images",
                "tags"
            )
        )
        sort_by = params.get("sort_by")
        sort_map = {
            "name.asc": "name",
            "name.desc": "-name",
            "created_at.asc": "created_at",
            "created_at.desc": "-created_at",
        }

        queryset = queryset.order_by(sort_map.get(sort_by, "-created_at"))

        return queryset.distinct()


@extend_schema(
    tags=["Recipient"],
    parameters=[
        OpenApiParameter("gender", OpenApiTypes.STR, description="Filter by gender: female, male, neutral")
    ]
)
class RecipientListView(ListAPIView):
    """
    List all recipients (Mother, Wife, Father, Brother, etc.)
    Can filter by gender to separate "Shop For Her" and "Shop For Him"
    
    Examples:
    - /recipients/ - All recipients
    - /recipients/?gender=female - Shop For Her
    - /recipients/?gender=male - Shop For Him
    """
    serializer_class = RecipientSerializer

    def get_queryset(self):
        queryset = Recipient.objects.filter(is_active=True)

        gender = self.request.query_params.get("gender")
        if gender in ['female', 'male', 'neutral']:
            queryset = queryset.filter(gender=gender)

        return queryset.order_by('display_order', 'name')


@extend_schema(tags=["Recipient"])
class RecipientDetailView(RetrieveAPIView):
    """
    Get details of a specific recipient
    Example: /recipients/mother/
    """
    serializer_class = RecipientSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Recipient.objects.filter(is_active=True)


@extend_schema(
    tags=["Recipient"],
    parameters=[
        OpenApiParameter("page", OpenApiTypes.INT),
        OpenApiParameter("sort_by", OpenApiTypes.STR, description="name.asc, name.desc, created_at.asc, created_at.desc"),
    ]
)
class ProductsByRecipientView(ListAPIView):
    """
    Get all products for a specific recipient with pagination
    Example: /recipients/mother/products/
    """
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        slug = self.kwargs["slug"]
        params = self.request.query_params

        queryset = (
            Product.objects
            .filter(recipients__slug=slug, is_active=True)
            .prefetch_related(
                "category",
                "category__categorygroup",
                "images",
                "tags"
            )
        )
        sort_by = params.get("sort_by")
        sort_map = {
            "name.asc": "name",
            "name.desc": "-name",
            "created_at.asc": "created_at",
            "created_at.desc": "-created_at",
        }

        queryset = queryset.order_by(sort_map.get(sort_by, "-created_at"))

        return queryset.distinct()