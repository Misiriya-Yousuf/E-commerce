from django import forms
from decimal import Decimal, InvalidOperation
from .models import Product,Category,ProductImage
from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']  # Only the 'name' field is needed for editing

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError('A category with this name already exists.')
        return name
    
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_variant']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("An image is required.")
        return image

class ProductForm(forms.ModelForm):
    main_image_upload = forms.ImageField(required=False, label="Main Image Upload")

    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'sale_price', 'discount_price', 'quantity', 'main_image']

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.cleaned_data.get('main_image_upload'):
            image = ProductImage.objects.create(image=self.cleaned_data['main_image_upload'], is_variant=False)
            product.main_image = image
        if commit:
            product.save()
        return product

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_trashed=False)

    def clean_sale_price(self):
        sale_price = self.cleaned_data.get('sale_price')
        
        # Ensure there is no extra whitespace
        if sale_price:
            sale_price = sale_price.strip()

        if not sale_price:
            raise forms.ValidationError("Sale price is required.")

        try:
            # Try to convert the sale price to Decimal
            sale_price = Decimal(sale_price)
            if sale_price <= 0:
                raise forms.ValidationError("Sale price must be greater than zero.")
        except (ValueError, InvalidOperation):
            raise forms.ValidationError("Sale price must be a valid decimal number.")
        
        return sale_price

    def clean_discount_price(self):
        discount_price = self.cleaned_data.get('discount_price')

        # Ensure there is no extra whitespace
        if discount_price:
            discount_price = discount_price.strip()

        if discount_price:
            try:
                # Try to convert the discount price to Decimal
                discount_price = Decimal(discount_price)
                if discount_price <= 0:
                    raise forms.ValidationError("Discount price must be greater than zero.")
            except (ValueError, InvalidOperation):
                raise forms.ValidationError("Discount price must be a valid decimal number.")
        
        return discount_price
