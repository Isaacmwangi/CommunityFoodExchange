# listings/models.py

from django.db import models
from django.contrib.auth.models import User

def listing_image_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/listings/images/<filename>
    return 'listings/images/{0}'.format(filename)

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  
    image = models.ImageField(upload_to=listing_image_path)  

    def __str__(self):
        return self.item_name
