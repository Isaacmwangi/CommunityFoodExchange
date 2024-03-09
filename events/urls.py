# events/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_event, name='create_event'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('upcoming/', views.upcoming_events, name='upcoming_events'),
    path('<int:event_id>/delete/', views.delete_event, name='delete_event'),  # New URL pattern
    path('<int:event_id>/rsvp/', views.event_rsvp, name='event_rsvp'),  
]
