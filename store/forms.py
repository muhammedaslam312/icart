from dataclasses import field
from django import forms
from .models import Product, ReviewRating, Variation


class ProductForm(forms.ModelForm):
    images = forms.ImageField(required=False, error_messages = {'invalid':("image files only")}, widget=forms.FileInput)
    class Meta:
        model = Product
        fields = ['product_name', 'description','price', 'discount_percent', 'images', 'stock', 'is_available', 'category',]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'     

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['product', 'variation_category', 'variation_value', 'is_active', ]     

    def __init__(self, *args, **kwargs):
        super(VariationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'              

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']            