# ratings_reviews\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('post_review/', views.post_review, name='post_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),  # Import delete_review from the correct module
    path('user_reviews/', views.user_reviews, name='user_reviews'),
]