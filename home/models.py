import imp
from django.db import models
from category.models import Category

# Create your models here.
class Banner(models.Model):
    banner = models.ImageField(upload_to='image/banners', null=True, blank=True)
    category    = models.ForeignKey(Category,on_delete=models.CASCADE,default=True)
    title       = models.CharField(max_length=100,default=True)
    is_first   = models.BooleanField(default=False)

    def get_banner_url(self):
        return self.banner.url
    def __str__(self):
        return self.title    