from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    cat_image = forms.ImageField(required=False, error_messages = {'invalid':("image files only")}, widget=forms.FileInput)
    class Meta:
        model = Category
        fields = ['category_name', 'discription','cat_image']

   

    def __init__(self,*args,**kwargs):
        super(CategoryForm,self).__init__(*args,**kwargs)

        # self.fields['main_category'].widget.attrs['class']='form-control form-control-user'

        self.fields['category_name'].widget.attrs['placeholder']='Enter Category name'
        self.fields['category_name'].widget.attrs['class']='form-control form-control-user'
        self.fields['category_name'].widget.attrs['type']='text'

        self.fields['discription'].widget.attrs['placeholder']='Enter Category discription'
        self.fields['discription'].widget.attrs['class']='form-control form-control-user'
        self.fields['discription'].widget.attrs['type']='text'
        self.fields['discription'].widget.attrs['row']=3
        
        self.fields['cat_image'].widget.attrs['placeholder']='Add images'
        self.fields['cat_image'].widget.attrs['class']='form-control'
        self.fields['cat_image'].widget.attrs['type']='file'

   