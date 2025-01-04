from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blocked = models.BooleanField(default=False)  # Field to mark if user is blocked

    def __str__(self):
        return self.user.username

class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)
    is_trashed = models.BooleanField(default=False)
    trashed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/images/')
    is_variant = models.BooleanField(default=False) 

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    main_image = models.ForeignKey(ProductImage, related_name='main_image', on_delete=models.SET_NULL, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete flag

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        """Return stock status."""
        return self.quantity > 0

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    variant_images = models.ManyToManyField(ProductImage, related_name='variant_images')

    def __str__(self):
        return f"Variant for {self.product.name} with {self.variant_images.count()} images"


