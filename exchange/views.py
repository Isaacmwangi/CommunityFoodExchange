# exchange/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ExchangeRequest
from .forms import ExchangeRequestForm
from listings.models import Listing
from django.http import HttpResponseBadRequest
from .models import ExchangeRequest
from messaging.models import Conversation

@login_required
def send_exchange_request(request, pk):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=pk)
        
        # Check if the user is trying to send a request to their own listing
        if listing.user == request.user:
            return HttpResponseBadRequest("You cannot send a request to your own listing.")
        
        # Check if the user has already sent a request for this listing
        existing_request = ExchangeRequest.objects.filter(sender=request.user, listing=listing).exists()
        if existing_request:
            return HttpResponseBadRequest("You have already sent a request for this listing.")
        
        form = ExchangeRequestForm(request.POST)
        if form.is_valid():
            exchange_request = form.save(commit=False)
            exchange_request.sender = request.user
            exchange_request.receiver = listing.user  # Set the receiver to the listing owner
            exchange_request.listing = listing
            exchange_request.save()
            return redirect('listing_detail', pk=pk)
    else:
        form = ExchangeRequestForm()
    return render(request, 'exchange/send_exchange_request.html', {'form': form})

@login_required
def exchange_requests(request):
    sent_requests = ExchangeRequest.objects.filter(sender=request.user)
    received_requests = ExchangeRequest.objects.filter(receiver=request.user)
    return render(request, 'exchange/exchange_requests.html', {'sent_requests': sent_requests, 'received_requests': received_requests})

@login_required
def manage_exchange_requests(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    exchange_requests = ExchangeRequest.objects.filter(listing=listing)
    is_owner = listing.user == request.user

    if not is_owner:
        return redirect('home')  # Only listing owner can manage requests

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        if action == 'accept':
            exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
            exchange_request.status = 'Accepted'
            exchange_request.save()
            # Create a conversation for the exchange
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, exchange_request.sender)
            return redirect('conversation_detail', conversation_id=conversation.id)

        elif action == 'reject':
            exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
            exchange_request.status = 'Rejected'
            exchange_request.save()
            return redirect('listing_detail', pk=pk)

        elif action == 'message':
            exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
            # Create a conversation for the exchange if not already existing
            conversation = Conversation.objects.filter(participants__in=[request.user, exchange_request.sender]).distinct().first()
            if not conversation:
                conversation = Conversation.objects.create()
                conversation.participants.add(request.user, exchange_request.sender)
            return redirect('send_message', conversation_id=conversation.id)

        elif action == 'delete':
            exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
            exchange_request.delete()
            return redirect('listing_detail', pk=pk)

        elif action == 'cancel':
            exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
            exchange_request.status = 'Cancelled'
            exchange_request.save()
            return redirect('listing_detail', pk=pk)

    return render(request, 'exchange/manage_exchange_requests.html', {'listing': listing, 'exchange_requests': exchange_requests})

@login_required
def accept_exchange_request(request, pk, request_id):
    # Fetch the listing and the exchange request
    listing = get_object_or_404(Listing, pk=pk)
    exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)

    # Check if the request is for the current user's listing
    if exchange_request.listing != listing or listing.user != request.user:
        return redirect('home')

    # Update the status of the exchange request to accepted
    exchange_request.status = 'Accepted'
    exchange_request.save()

    # Create a conversation for the exchange
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, exchange_request.sender)

    # Redirect to the conversation detail view
    return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
def cancel_exchange_request(request, pk, request_id):
    # Fetch the listing and the exchange request
    listing = get_object_or_404(Listing, pk=pk)
    exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)

    # Check if the request is for the current user's listing
    if exchange_request.listing != listing or listing.user != request.user:
        return redirect('home')

    # Update the status of the exchange request to cancel
    exchange_request.status = 'Cancelled'
    exchange_request.save()

    return redirect('listing_detail', pk=pk)

