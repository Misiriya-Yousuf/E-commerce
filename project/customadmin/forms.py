from django import forms
from .models import Product 

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'sale_price', 'discount_price', 'quantity', 'image']

