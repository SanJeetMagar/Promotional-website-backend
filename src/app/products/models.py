from django.db import models
from django.utils.text import slugify
from src.app.common.models import Basemodel


class MainCategory(Basemodel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name


class Category(Basemodel):
    categorygroup = models.ForeignKey(
        MainCategory, 
        on_delete=models.CASCADE, 
        related_name="categories"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return f"{self.categorygroup.name} → {self.name}"


class Tag(Basemodel):
    name = models.CharField()
    
    def __str__(self) -> str:
        return f"{self.name}"


class Occasion(Basemodel):
    """
    Model for special occasions like Father's Day, Dashain, Tihar, etc.
    Used in 'Shop By Occasion' section
    """
    title = models.CharField(max_length=255)
    short_description = models.TextField()
    image = models.ImageField(
        upload_to="occasions/",
        help_text="Occasion banner image"
    )
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Show/hide this occasion on the website"
    )
    display_order = models.IntegerField(
        default=0,
        help_text="Lower numbers appear first"
    )

    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = "Occasion"
        verbose_name_plural = "Occasions"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            candidate = base
            counter = 1
            while Occasion.objects.filter(slug=candidate).exists():
                candidate = f"{base}-{counter}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)


class Recipient(Basemodel):
    """
    Model for gift recipients like Mother, Wife, Father, Brother, etc.
    Used in 'Shop For Her' and 'Shop For Him' sections
    """
    GENDER_CHOICES = [
        ('female', 'Female'),  # For "Shop For Her"
        ('male', 'Male'),      # For "Shop For Him"
        ('neutral', 'Gender Neutral'),
    ]

    name = models.CharField(
        max_length=255,
        help_text="e.g., Mother, Wife, Father, Brother"
    )
    slug = models.SlugField(unique=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='neutral'
    )
    tagline = models.CharField(
        max_length=255,
        help_text="e.g., 'For the one who means everything', 'Your life partner'"
    )
    image = models.ImageField(
        upload_to="recipients/",
        help_text="Recipient category image"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Show/hide this recipient on the website"
    )
    display_order = models.IntegerField(
        default=0,
        help_text="Lower numbers appear first"
    )

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Recipient"
        verbose_name_plural = "Recipients"

    def __str__(self):
        return f"{self.name} ({self.get_gender_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            candidate = base
            counter = 1
            while Recipient.objects.filter(slug=candidate).exists():
                candidate = f"{base}-{counter}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)


class Product(Basemodel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ManyToManyField(Category, related_name="products")
    short_description = models.TextField()
    full_description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    
    # Colors and Materials
    colors = models.JSONField(
        default=list,
        blank=True,
        help_text='List of color objects: [{"name": "Terracotta", "hex": "#E2725B"}]'
    )
    materials = models.JSONField(
        default=list,
        blank=True,
        help_text='List of materials: ["Ceramic", "Wood", "Metal"]'
    )
    
    # 3D Model field
    model_3d = models.FileField(
        upload_to="products/3d_models/",
        blank=True,
        null=True,
        help_text="3D model file (.glb, .gltf format recommended)"
    )
    
    # Link products to occasions and recipients
    occasions = models.ManyToManyField(
        Occasion,
        related_name="products",
        blank=True,
        help_text="Which occasions is this product suitable for?"
    )
    recipients = models.ManyToManyField(
        Recipient,
        related_name="products",
        blank=True,
        help_text="Who is this product for? (Mother, Father, etc.)"
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "product"
            slug_candidate = base
            i = 1
            while Product.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base}-{i}"
                i += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

class ProductImage(Basemodel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.product.name} image"


class Specification(Basemodel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specifications"
    )
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.product.name} - {self.label}: {self.value}"


class KeyFeature(Basemodel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="keyfeatures"
    )
    text = models.TextField()

    def __str__(self) -> str:
        return f"{self.product.name} - {self.text}"