from django import forms
from .models import Product,Profile

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_image', 'rupees', 'product_offer', 'review', 'rating']

class Profileform(forms.ModelForm):
    class Meta:
        model=Profile
        fields='__all__'
        exclude = ["user"]