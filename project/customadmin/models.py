from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blocked = models.BooleanField(default=False)  # Field to mark if user is blocked

    def __str__(self):
        return self.user.username
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
    is_deleted = models.BooleanField(default=False)  # Soft delete flag

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        """Return stock status."""
        return self.quantity > 0

