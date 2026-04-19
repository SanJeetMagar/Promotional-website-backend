from django.contrib import admin
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


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'categorygroup', 'slug', 'created_at']
    list_filter = ['categorygroup']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'categorygroup__name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


# ============ PRODUCT ADMIN WITH INLINES ============

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text']


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1
    fields = ['label', 'value']


class KeyFeatureInline(admin.TabularInline):
    model = KeyFeature
    extra = 1
    fields = ['text']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'slug', 
        'is_active', 
        'is_featured', 
        'is_popular',
        'has_3d_model',
        'created_at'
    ]
    list_filter = [
        'is_active', 
        'is_featured', 
        'is_popular', 
        'category',
        'occasions',
        'recipients'
    ]
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'short_description']
    filter_horizontal = ['category', 'tags', 'occasions', 'recipients']
    
    inlines = [ProductImageInline, SpecificationInline, KeyFeatureInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'tags')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'full_description')
        }),
        ('Product Details', {
            'fields': ('colors', 'materials'),
            'description': 'Colors format: [{"name": "Terracotta", "hex": "#E2725B"}]. Materials format: ["Ceramic", "Wood"]'
        }),
        ('Media', {
            'fields': ('model_3d',),
            'description': 'Upload 3D model file (.glb or .gltf format recommended)'
        }),
        ('Classification', {
            'fields': ('occasions', 'recipients'),
            'description': 'Associate this product with occasions and recipients'
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_popular')
        }),
    )
    
    def has_3d_model(self, obj):
        """Show if product has a 3D model"""
        return bool(obj.model_3d)
    has_3d_model.boolean = True
    has_3d_model.short_description = '3D Model'


# ============ OCCASION ADMIN ============

@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'slug',
        'is_active',
        'display_order',
        'product_count',
        'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'short_description']
    list_editable = ['is_active', 'display_order']
    ordering = ['display_order', 'title']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('is_active', 'display_order'),
            'description': 'Lower display_order numbers appear first'
        }),
    )
    
    def product_count(self, obj):
        """Show how many products are linked to this occasion"""
        return obj.products.filter(is_active=True).count()
    product_count.short_description = 'Active Products'


# ============ RECIPIENT ADMIN ============

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'gender',
        'slug',
        'is_active',
        'display_order',
        'product_count',
        'created_at'
    ]
    list_filter = ['gender', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'tagline']
    list_editable = ['is_active', 'display_order']
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'gender', 'tagline')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('is_active', 'display_order'),
            'description': 'Lower display_order numbers appear first'
        }),
    )
    
    def product_count(self, obj):
        """Show how many products are linked to this recipient"""
        return obj.products.filter(is_active=True).count()
    product_count.short_description = 'Active Products'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'alt_text', 'created_at']
    list_filter = ['product']
    search_fields = ['product__name', 'alt_text']


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ['product', 'label', 'value', 'created_at']
    list_filter = ['product']
    search_fields = ['product__name', 'label', 'value']


@admin.register(KeyFeature)
class KeyFeatureAdmin(admin.ModelAdmin):
    list_display = ['product', 'text', 'created_at']
    list_filter = ['product']
    search_fields = ['product__name', 'text']