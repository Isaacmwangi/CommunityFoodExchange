# exchange/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ExchangeRequest
from .forms import ExchangeRequestForm
from listings.models import Listing

@login_required
def send_exchange_request(request, listing_id):
    if request.method == 'POST':
        form = ExchangeRequestForm(request.POST)
        if form.is_valid():
            listing = Listing.objects.get(pk=listing_id)  # Fetch the listing
            exchange_request = form.save(commit=False)
            exchange_request.sender = request.user
            exchange_request.receiver = listing.user  # Set the receiver to the listing's user
            exchange_request.listing_id = listing_id
            exchange_request.save()
            return redirect('home')
    else:
        form = ExchangeRequestForm()
    return render(request, 'exchange/send_exchange_request.html', {'form': form})



@login_required
def exchange_requests(request):
    sent_requests = ExchangeRequest.objects.filter(sender=request.user)
    received_requests = ExchangeRequest.objects.filter(receiver=request.user)
    return render(request, 'exchange/exchange_requests.html', {'sent_requests': sent_requests, 'received_requests': received_requests})

