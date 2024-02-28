# accounts/models.py

from django.db import models
from django.contrib.auth.models import User

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
        return Message.objects.filter(conversation__participants=self, read=False).count()