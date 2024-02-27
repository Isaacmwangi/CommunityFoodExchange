from django.shortcuts import render
from .models import Message

def messages(request):
    conversations = Message.objects.filter(sender=request.user).distinct('receiver')
    return render(request, 'messaging/messages.html', {'conversations': conversations})

def conversation(request, receiver_id):
    messages = Message.objects.filter(sender=request.user, receiver_id=receiver_id) | Message.objects.filter(sender_id=receiver_id, receiver=request.user)
    return render(request, 'messaging/conversation.html', {'messages': messages})
