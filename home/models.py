from django.db import models

# Create your models here.
class Banner(models.Model):
    banner = models.ImageField(upload_to='image/banners', null=True, blank=True)

    def get_banner_url(self):
        return self.banner.url