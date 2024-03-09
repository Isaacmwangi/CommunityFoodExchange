# ratings_reviews/models.py

from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)