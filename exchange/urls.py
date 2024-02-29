# exchange/urls.py

from django.urls import path
from .views import send_exchange_request, exchange_requests, manage_exchange_requests, accept_exchange_request, cancel_exchange_request

urlpatterns = [
    path('send/<int:pk>/', send_exchange_request, name='send_exchange_request'),
    path('requests/', exchange_requests, name='exchange_requests'),
    path('<int:pk>/accept_request/<int:request_id>/', accept_exchange_request, name='accept_exchange_request'),
    path('<int:pk>/cancel_request/<int:request_id>/', cancel_exchange_request, name='cancel_exchange_request'),
    path('<int:pk>/manage_exchange_requests/', manage_exchange_requests, name='manage_exchange_requests'),
]
