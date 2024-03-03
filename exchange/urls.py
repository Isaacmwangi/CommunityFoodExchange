# exchange/urls.py

from django.urls import path
from .views import (
    send_exchange_request,
    exchange_requests,
    manage_exchange_requests,
    accept_exchange_request,
    cancel_exchange_request,
    cancelled_requests,
    accepted_requests,
    rejected_requests,
    exchange_request_detail, 
    my_requests,
    received_requests,
    trend_analysis,)

urlpatterns = [
    path('send/<int:pk>/', send_exchange_request, name='send_exchange_request'),
    path('requests/', exchange_requests, name='exchange_requests'),
    path('<int:pk>/accept_request/<int:request_id>/', accept_exchange_request, name='accept_exchange_request'),
    path('<int:pk>/cancel_request/<int:request_id>/', cancel_exchange_request, name='cancel_exchange_request'),
    path('<int:pk>/manage_exchange_requests/', manage_exchange_requests, name='manage_exchange_requests'),
    path('cancelled-requests/', cancelled_requests, name='cancelled_requests'),
    path('accepted-requests/', accepted_requests, name='accepted_requests'),
    path('rejected-requests/', rejected_requests, name='rejected_requests'),
    path('<int:request_id>/', exchange_request_detail, name='exchange_request_detail'),  # Define URL pattern for exchange request detail
    path('exchange_request_detail/<int:request_id>/', exchange_request_detail, name='exchange_request_detail'),
    path('trend-analysis/', trend_analysis, name='trend_analysis'),  # URL for generating trend analysis graph
    path('my-requests/', my_requests, name='my_requests'),
    path('received-requests/', received_requests, name='received_requests'),
    path('trend-analysis/image/', trend_analysis, name='trend_analysis_image'),  # URL for serving trend analysis image
    # Define other URLs as needed
]
