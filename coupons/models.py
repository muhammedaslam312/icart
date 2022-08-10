from re import T
from django.db import models

# Create your models here.

class Coupon(models.Model):
    code = models.CharField(primary_key=True,max_length=50)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)
    
    
    def __str__(self):
        return self.code