from django import forms
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
        # Customize the category dropdown to show only active categories
        self.fields['category'].queryset = Category.objects.filter(is_trashed=False)
       
    def clean_sale_price(self):
        sale_price = self.cleaned_data.get('sale_price')
        if sale_price is not None and sale_price <= 0:
            raise forms.ValidationError("Sale price must be greater than zero.")
        return sale_price

    def clean_discount_price(self):
        discount_price = self.cleaned_data.get('discount_price')
        if discount_price is not None and discount_price <= 0:
            raise forms.ValidationError("Discount price must be greater than zero.")
        return discount_price
