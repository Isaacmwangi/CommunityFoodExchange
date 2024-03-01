# accounts/models.py

from django.db import models
from django.contrib.auth.models import User
from messaging.models import Message  # Import the Message model from messaging app

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    dietary_preferences = models.CharField(max_length=200)
    food_allergies = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


class UserWithUnreadMessagesCount(User):
    @property
    def unread_messages_count(self):
        return Message.objects.filter(conversation__participants=self, is_read=False).count()  # Assuming is_read is the field indicating whether a message is read or not
