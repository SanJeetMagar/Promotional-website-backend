from rest_framework import serializers
from .models import (
    MainCategory,
    Category,
    Product,
    ProductImage,
    Specification,
    KeyFeature,
    Tag,
    Occasion,
    Recipient,
)


class NestedCategorySerializer(serializers.ModelSerializer):
    main_category = serializers.CharField(source="categorygroup.slug", read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "main_category"]


class MegaMenuSerializer(serializers.ModelSerializer):
    categories = NestedCategorySerializer(many=True, read_only=True)

    class Meta:
        model = MainCategory
        fields = ["id", "name", "slug", "categories"]


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ["id", "label", "value"]


class KeyFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyFeature
        fields = ["id", "text"]


class ProductListSerializer(serializers.ModelSerializer):
    """Used for product listings in grids/cards"""
    primary_image = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    categories = NestedCategorySerializer(many=True, read_only=True, source="category")
    tags = TagSerializer(many=True, read_only=True)
    model_3d = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "primary_image",
            "images",
            "categories",
            "tags",
            "short_description",
            "colors",
            "materials",
            "is_featured",
            "is_popular",
            "model_3d",
        ]

    def get_primary_image(self, obj):
        request = self.context.get("request")

        if getattr(obj, "primary_image_url", None):
            url = obj.primary_image_url
            return request.build_absolute_uri(url) if request else url

        first_img = obj.images.first()
        if first_img and first_img.image:
            url = first_img.image.url
            return request.build_absolute_uri(url) if request else url

        return None

    def get_model_3d(self, obj):
        request = self.context.get("request")
        if obj.model_3d:
            url = obj.model_3d.url
            return request.build_absolute_uri(url) if request else url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Used for single product detail page"""
    images = ProductImageSerializer(many=True, read_only=True)
    categories = NestedCategorySerializer(many=True, read_only=True, source="category")
    specifications = SpecificationSerializer(many=True, read_only=True)
    keyfeatures = KeyFeatureSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    model_3d = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "short_description",
            "full_description",
            "is_active",
            "categories",
            "images",
            "specifications",
            "keyfeatures",
            "tags",
            "colors",
            "materials",
            "is_featured",
            "is_popular",
            "model_3d",
        ]

    def get_model_3d(self, obj):
        request = self.context.get("request")
        if obj.model_3d:
            url = obj.model_3d.url
            return request.build_absolute_uri(url) if request else url
        return None
# ============ NEW: OCCASION SERIALIZERS ============

class OccasionSerializer(serializers.ModelSerializer):
    """
    Serializer for Occasion model
    Used for listing all occasions (Father's Day, Dashain, etc.)
    """
    image = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Occasion
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "image",
            "product_count",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_product_count(self, obj):
        """Return count of active products for this occasion"""
        return obj.products.filter(is_active=True).count()


# ============ NEW: RECIPIENT SERIALIZERS ============

class RecipientSerializer(serializers.ModelSerializer):
    """
    Serializer for Recipient model
    Used for listing recipients (Mother, Father, Wife, etc.)
    """
    image = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipient
        fields = [
            "id",
            "name",
            "slug",
            "gender",
            "tagline",
            "image",
            "product_count",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_product_count(self, obj):
        """Return count of active products for this recipient"""
        return obj.products.filter(is_active=True).count()


class RecipientDetailSerializer(RecipientSerializer):
    """
    Extended serializer with more details
    Can be used if you need more info on detail pages
    """
    class Meta(RecipientSerializer.Meta):
        fields = RecipientSerializer.Meta.fields + ["is_active", "display_order"]