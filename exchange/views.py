# exchange/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ExchangeRequest
from .forms import ExchangeRequestForm, CancelExchangeRequestForm
from listings.models import Listing
from django.http import HttpResponseBadRequest
from messaging.models import Conversation
import matplotlib.pyplot as plt
from django.db.models import Count
from django.utils.timezone import datetime, timedelta
from django.http import HttpResponse
from io import BytesIO
from django.conf import settings
import matplotlib
matplotlib.use('Agg')  # Use Agg backend to avoid "RuntimeError: main thread is not in main loop"
from django.http import Http404


@login_required
def send_exchange_request(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    receiver = listing.user  # Get the user who posted the listing

    if request.method == 'POST':
        if listing.user == request.user:
            return HttpResponseBadRequest("You cannot send a request to your own listing.")
        existing_request = ExchangeRequest.objects.filter(sender=request.user, listing=listing).exists()
        if existing_request:
            return HttpResponseBadRequest("You have already sent a request for this listing.")
        form = ExchangeRequestForm(request.POST)
        if form.is_valid():
            exchange_request = form.save(commit=False)
            exchange_request.sender = request.user
            exchange_request.receiver = receiver  # Set the receiver
            exchange_request.listing = listing
            exchange_request.save()
            return redirect('listing_detail', pk=pk)
    else:
        form = ExchangeRequestForm()
    return render(request, 'exchange/send_exchange_request.html', {'form': form, 'receiver': receiver})

@login_required
def exchange_requests(request):
    # Separate exchange requests into sent and received
    sent_requests = ExchangeRequest.objects.filter(sender=request.user).order_by('-created_at')
    received_requests = ExchangeRequest.objects.filter(receiver=request.user).order_by('-created_at')
    
    # Count the number of sent and received requests
    sent_count = sent_requests.count()
    received_count = received_requests.count()
    
    # Calculate the total count of requests
    total_requests = sent_count + received_count
    
    # Count the number of accepted, rejected, and cancelled requests
    accepted_count = ExchangeRequest.objects.filter(receiver=request.user, status='Accepted').count()
    rejected_count = ExchangeRequest.objects.filter(receiver=request.user, status='Rejected').count()
    cancelled_count = ExchangeRequest.objects.filter(receiver=request.user, status='Cancelled').count()
    
    return render(request, 'exchange/exchange_requests.html', {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'sent_count': sent_count,
        'received_count': received_count,
        'total_requests': total_requests,
        'accepted_count': accepted_count,  # Add counts for accepted, rejected, and cancelled requests
        'rejected_count': rejected_count,
        'cancelled_count': cancelled_count,
    })


@login_required
def accepted_requests(request):
    accepted_requests = ExchangeRequest.objects.filter(receiver=request.user, status='Accepted').order_by('-created_at')
    accepted_count = accepted_requests.count()
    return render(request, 'exchange/accepted_requests.html', {'accepted_requests': accepted_requests, 'accepted_count': accepted_count})

@login_required
def rejected_requests(request):
    rejected_requests = ExchangeRequest.objects.filter(receiver=request.user, status='Rejected').order_by('-created_at')
    rejected_count = rejected_requests.count()
    return render(request, 'exchange/rejected_requests.html', {'rejected_requests': rejected_requests, 'rejected_count': rejected_count})

@login_required
def cancelled_requests(request):
    cancelled_requests = ExchangeRequest.objects.filter(receiver=request.user, status='Cancelled').order_by('-created_at')
    cancelled_count = cancelled_requests.count()
    return render(request, 'exchange/cancelled_requests.html', {'cancelled_requests': cancelled_requests, 'cancelled_count': cancelled_count})






login_required
def my_requests(request):
    sent_requests = ExchangeRequest.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'exchange/my_requests.html', {'sent_requests': sent_requests})

@login_required
def received_requests(request):
    received_requests = ExchangeRequest.objects.filter(receiver=request.user).order_by('-created_at')
    total_requests = received_requests.count()  # Calculate the total number of requests
    return render(request, 'exchange/received_requests.html', {'received_requests': received_requests, 'total_requests': total_requests})


@login_required
def trend_analysis(request):
    # Query to get the count of exchange requests for each status grouped by date
    trends = ExchangeRequest.objects.filter(status__in=['Accepted', 'Rejected', 'Cancelled'], created_at__gte=datetime.now()-timedelta(days=7)) \
                        .values('status') \
                        .annotate(count=Count('id')) \
                        .order_by('status')

    # Extract data for the trend graph
    statuses = [t['status'] for t in trends]
    counts = [t['count'] for t in trends]

    # Generate the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(statuses, counts, color=['green', 'red', 'blue'])  # Use different colors for each status
    plt.title('Exchange Request Trend (Last 7 Days)')
    plt.xlabel('Status')
    plt.ylabel('Number of Requests')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a PNG image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()

    # Set the buffer pointer to the beginning
    buffer.seek(0)

    # Return the plot as an HTTP response
    return HttpResponse(buffer.getvalue(), content_type='image/png')





@login_required
def exchange_request_detail(request, request_id):
    exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
    return render(request, 'exchange/exchange_request_detail.html', {'exchange_request': exchange_request})


from django.http import Http404

@login_required
def manage_exchange_requests(request, pk):
    try:
        listing = Listing.objects.get(pk=pk)
    except Listing.DoesNotExist:
        # Handle the case where the listing with the provided pk does not exist
        # Redirect the user to the home page or the previous page
        return redirect('home')  # Or replace 'home' with the appropriate URL name

    exchange_requests = ExchangeRequest.objects.filter(listing=listing)
    is_owner = listing.user == request.user
    if not is_owner:
        return redirect('home')
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        if action == 'accept':
            exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
            exchange_request.status = 'Accepted'
            exchange_request.save()
            return redirect('listing_detail', pk=pk)
        elif action == 'reject':
            exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
            exchange_request.status = 'Rejected'
            exchange_request.save()
            return redirect('listing_detail', pk=pk)
        elif action == 'message':
            exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
            conversation = Conversation.objects.filter(participants__in=[request.user, exchange_request.sender]).first()
            if not conversation:
                # If conversation doesn't exist, create a new one
                conversation = Conversation.objects.create()
                conversation.participants.add(request.user, exchange_request.sender)
            return redirect('conversation_detail', conversation_id=conversation.id)
        elif action == 'cancel':
            exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
            form = CancelExchangeRequestForm(request.POST, instance=exchange_request)
            if form.is_valid():
                form.save()
                exchange_request.status = 'Cancelled'
                exchange_request.save()
                return redirect('listing_detail', pk=pk)
    else:
        form = CancelExchangeRequestForm()
    return render(request, 'exchange/manage_exchange_requests.html', {'listing': listing, 'exchange_requests': exchange_requests, 'form': form})





@login_required
def accept_exchange_request(request, pk, request_id):
    listing = get_object_or_404(Listing, pk=pk)
    exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
    if exchange_request.listing != listing or listing.user != request.user:
        return redirect('home')
    exchange_request.status = 'Accepted'
    exchange_request.save()
    return redirect('conversation_detail', conversation_id=exchange_request.conversation.id)

@login_required
def cancel_exchange_request(request, pk, request_id):
    listing = get_object_or_404(Listing, pk=pk)
    exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
    if exchange_request.listing != listing or listing.user != request.user:
        return redirect('home')
    if request.method == 'POST':
        form = CancelExchangeRequestForm(request.POST, instance=exchange_request)
        if form.is_valid():
            form.save()
            exchange_request.status = 'Cancelled'
            exchange_request.save()
            return redirect('listing_detail', pk=pk)
    else:
        form = CancelExchangeRequestForm(instance=exchange_request)
    return render(request, 'exchange/cancel_exchange_request.html', {'form': form})


