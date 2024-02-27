from django.urls import path
from .views import create_event, upcoming_events

urlpatterns = [
    path('create/', create_event, name='create_event'),
    path('upcoming/', upcoming_events, name='upcoming_events'),
]
