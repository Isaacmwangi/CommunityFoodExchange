# listings/models.py

from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    expiration_date = models.DateField()

    def __str__(self):
        return self.item_name
