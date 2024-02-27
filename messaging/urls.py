from django.urls import path
from .views import messages, conversation

urlpatterns = [
    path('messages/', messages, name='messages'),
    path('conversation/<int:receiver_id>/', conversation, name='conversation'),
]
