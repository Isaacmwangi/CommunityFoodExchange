# exchange/urls.py

from django.urls import path
from .views import send_exchange_request, exchange_requests

urlpatterns = [
    path('send/<int:pk>/', send_exchange_request, name='send_exchange_request'),
    path('requests/', exchange_requests, name='exchange_requests'),
]

