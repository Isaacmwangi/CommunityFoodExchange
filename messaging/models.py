# messaging/models.py
from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing
from cloudinary.models import CloudinaryField

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='conversations', blank=True, null=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    file = CloudinaryField('file', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    MESSAGE_TYPES = (
        ('ER', 'Exchange Request'),
        ('IA', 'Item Added'),
        ('DM', 'Direct Message'),
        ('CM', 'Channel Message'),
    )
    message_type = models.CharField(max_length=2, choices=MESSAGE_TYPES, default='DM')





