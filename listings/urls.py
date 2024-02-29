# listings/urls.py

from django.urls import path
from .views import listing_create, listing_detail, listing_update, listing_delete, accept_exchange_request, cancel_exchange_request

urlpatterns = [
    path('create/', listing_create, name='listing_create'),
    path('<int:pk>/', listing_detail, name='listing_detail'),
    path('<int:pk>/update/', listing_update, name='listing_update'),
    path('<int:pk>/delete/', listing_delete, name='listing_delete'),
    path('<int:pk>/accept_request/<int:request_id>/', accept_exchange_request, name='accept_exchange_request'),
    path('<int:pk>/cancel_request/<int:request_id>/', cancel_exchange_request, name='cancel_exchange_request'),]
