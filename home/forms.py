
from django import forms
from .models import Banner



class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['category','title','banner','is_first']