# exchange/models.py

from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing

class ExchangeRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchange_sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchange_received_requests')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason_for_cancellation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.listing.item_name}'
