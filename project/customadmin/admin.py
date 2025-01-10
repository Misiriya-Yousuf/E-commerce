from django.contrib import admin
from .models import UserProfile, Product, Category,ProductVariant,ProductImage


# UserProfile Admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blocked')  # Display fields in the admin list view
    search_fields = ('user__username',)  # Add search functionality

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    fields = ['category', 'name', 'description', 'sale_price', 'discount_price', 'coupon_code', 'quantity', 'main_image', 'is_deleted']
    list_display = ['name', 'category', 'sale_price', 'coupon_code', 'quantity', 'is_deleted']
    list_filter = ('category', 'is_deleted')  
    search_fields = ('name', 'category__name') 

    def clean_coupon_code(self):
        coupon_code = self.cleaned_data.get('coupon_code')
        if not coupon_code:
            return None  
        return coupon_code


# ProductVariant Admin
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_product_name', 'get_variant_images')  # Show ID, product name, and images
    search_fields = ('product__name', 'variant_images__id')  # Search by product name and image IDs
    filter_horizontal = ('variant_images',)  # Use a horizontal filter widget for variant images

    def get_variant_images(self, obj):
        """Display the images of the variant in the list view."""
        images = obj.variant_images.all()
        if images.exists():
            return ", ".join([f"Image ID: {image.id}" for image in images])
        return "No images"
    get_variant_images.short_description = 'Variant Images'

    def get_product_name(self, obj):
        """Display the related product name."""
        return obj.product.name
    get_product_name.short_description = 'Product Name'


# ProductColor Admin

# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_trashed', 'trashed_at')  # Show key details
    list_filter = ('is_trashed',)  # Filter by trashed status
    search_fields = ('name',)  # Add search functionality

# Productimage Admin
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'is_variant')  # Display image ID and variant status
    list_filter = ('is_variant',)  # Filter by variant (main image or variant image)
    search_fields = ('id',)  # Enable searching by image ID

# Register models with admin site
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage,ProductImageAdmin)

