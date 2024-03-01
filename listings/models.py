# listings/models.py

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

def listing_image_path(instance, filename):
    return f'listings/{instance.user.username}/{filename}'

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  
    image = CloudinaryField('image')  # Removed upload_to argument

    def __str__(self):
        return self.item_name

