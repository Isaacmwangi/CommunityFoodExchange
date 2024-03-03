# messaging/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation
from .forms import MessageForm
from .models import Conversation
from listings.models import Listing



@login_required
def conversation_list(request):
    conversations = request.user.conversations.all()
    for conversation in conversations:
        conversation.latest_message = conversation.messages.last()
        conversation.unread_messages_count = conversation.messages.filter(sender=request.user, is_read=False).count()
        conversation.new_messages_count = conversation.messages.exclude(sender=request.user).filter(is_read=False).count()
        # Determine the other participant in the conversation
        conversation.other_user = conversation.participants.exclude(id=request.user.id).first()
        # Assuming each conversation is associated with a listing
        conversation.listing = Listing.objects.first()  # Replace with your actual logic to retrieve the listing
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})



@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user not in conversation.participants.all():
        return redirect('conversation_list')
    messages = conversation.messages.all().order_by('timestamp')
    # Mark messages as read when viewing the conversation detail
    for message in messages:
        if message.sender != request.user:
            message.is_read = True
            message.save()
    # Determine the other participant in the conversation
    other_user = conversation.participants.exclude(id=request.user.id).first()
    # Retrieve the listing associated with the conversation
    listing = conversation.listing  # Adjust this line
    return render(request, 'messaging/conversation_detail.html', {'conversation': conversation, 'messages': messages, 'other_user': other_user, 'listing': listing})

@login_required
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            return redirect('conversation_detail', conversation_id=conversation_id)
    else:
        form = MessageForm()
    return render(request, 'messaging/send_message.html', {'form': form})

