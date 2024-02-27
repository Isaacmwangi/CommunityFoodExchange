# listings/urls.py

from django.urls import path
from .views import listing_create, listing_update, listing_delete

urlpatterns = [
    path('create/', listing_create, name='listing_create'),
    path('<int:pk>/update/', listing_update, name='listing_update'),
    path('<int:pk>/delete/', listing_delete, name='listing_delete'),
]
