


from django.urls import reverse


from category.models import Category
from django.db import models
from accounts.models import Account
from django.db.models import Avg, Count

# Create your models here.


class Product(models.Model):
    product_name  = models.CharField(max_length=200,unique=True)
    slug          = models.SlugField(max_length=200, unique=True)
    description   = models.TextField(max_length=500, blank=True)
    price         = models.FloatField()
    discount_percent = models.FloatField(default=0)
    images         = models.ImageField(upload_to='photos/products')
    stock         = models.BigIntegerField()
    is_available  = models.BooleanField(default=True)
    category      = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date  = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    is_shipped = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    @property
    def discount(self):
        if self.discount_percent > 0:
            discounted_price = self.price - self.price * self.discount_percent / 100
            return discounted_price

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg        

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    
    def get_url(self):
        return reverse('products_detail',args=[self.category.slug,self.slug])
    def __str__(self):
        return self.product_name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def storages(self):
        return super(VariationManager, self).filter(variation_category='storage', is_active=True)    


variation_category_choice =(
    ('color', 'color'),
    ('storage', 'storage'),

)
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices= variation_category_choice)
    variation_value   =models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'products',max_length = 225)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery' 

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=100, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
