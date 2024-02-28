# messaging/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from .forms import MessageForm

@login_required
def conversation_list(request):
    conversations = request.user.conversations.all()
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user not in conversation.participants.all():
        return redirect('conversation_list')
    messages = conversation.messages.all()
    # Mark messages as read when viewing the conversation detail
    for message in messages:
        if message.sender != request.user:
            message.is_read = True
            message.save()
    return render(request, 'messaging/conversation_detail.html', {'conversation': conversation, 'messages': messages})

@login_required
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user not in conversation.participants.all():
        return redirect('conversation_list')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
    return render(request, 'messaging/send_message.html', {'form': form})
