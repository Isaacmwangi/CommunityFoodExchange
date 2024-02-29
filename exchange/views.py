# exchange/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ExchangeRequest
from .forms import ExchangeRequestForm
from listings.models import Listing
from django.http import HttpResponseBadRequest
from exchange.models import ExchangeRequest



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


