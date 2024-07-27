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
from django.contrib import messages 

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

@login_required
def cancel_exchange_request(request, pk, request_id):
    listing = get_object_or_404(Listing, pk=pk)
    exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
    if exchange_request.listing != listing or listing.user != request.user:
        return redirect('home')
    if request.method == 'POST':
        exchange_request.status = 'Cancelled'
        exchange_request.save()
        messages.success(request, 'Exchange request cancelled successfully.')
        return redirect('listing_detail', pk=pk)
    return render(request, 'exchange/cancel_exchange_request.html', {'exchange_request': exchange_request})






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
    trends_received = ExchangeRequest.objects.filter(receiver=request.user, created_at__gte=datetime.now()-timedelta(days=7)) \
                        .values('status') \
                        .annotate(count=Count('id')) \
                        .order_by('status')

    trends_sent = ExchangeRequest.objects.filter(sender=request.user, created_at__gte=datetime.now()-timedelta(days=7)) \
                        .values('status') \
                        .annotate(count=Count('id')) \
                        .order_by('status')

    # Initialize counts for received and sent requests
    received_counts = {'Accepted': 0, 'Rejected': 0, 'Cancelled': 0, 'Pending': 0}
    sent_counts = {'Accepted': 0, 'Rejected': 0, 'Cancelled': 0, 'Pending': 0}

    # Define colors for each status
    status_colors = {'Accepted': 'green', 'Rejected': 'red', 'Cancelled': 'blue', 'Pending': 'gray'}

    # Populate counts for received requests
    for trend in trends_received:
        status = trend['status']
        count = trend['count']
        received_counts[status] = count

    # Populate counts for sent requests
    for trend in trends_sent:
        status = trend['status']
        count = trend['count']
        sent_counts[status] = count

    # Generate the bar graphs
    plt.figure(figsize=(12, 6))

    # Plot for received requests
    plt.subplot(1, 2, 1)
    plt.bar(received_counts.keys(), received_counts.values(), color=[status_colors.get(status, 'gray') for status in received_counts.keys()])
    plt.title('Received Exchange Request Trend (Last 7 Days)')
    plt.xlabel('Status')
    plt.ylabel('Number of Requests')
    plt.xticks(rotation=45)

    # Plot for sent requests
    plt.subplot(1, 2, 2)
    plt.bar(sent_counts.keys(), sent_counts.values(), color=[status_colors.get(status, 'gray') for status in sent_counts.keys()])
    plt.title('Sent Exchange Request Trend (Last 7 Days)')
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
        return redirect('home')  # Redirect if listing does not exist

    exchange_requests = ExchangeRequest.objects.filter(listing=listing)
    is_owner = listing.user == request.user
    if not is_owner:
        return redirect('home')

    form = CancelExchangeRequestForm()

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
            # Check if conversation already exists between users
            conversation = exchange_request.conversation
            if not conversation:
                # Create new conversation if it doesn't exist
                conversation = Conversation.objects.create()
                conversation.participants.add(request.user, exchange_request.sender)
                exchange_request.conversation = conversation
                exchange_request.save()
            return redirect('conversation_detail', conversation_id=conversation.id)
        elif action == 'cancel':
            exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
            if request.method == 'POST':
                form = CancelExchangeRequestForm(request.POST, instance=exchange_request)
                if form.is_valid():
                    exchange_request.status = 'Cancelled'
                    exchange_request.save()
                    messages.success(request, 'Exchange request cancelled successfully.')
                    return redirect('listing_detail', pk=pk)
            else:
                return render(request, 'exchange/cancel_exchange_request.html', {'form': form, 'exchange_request': exchange_request})

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
    if exchange_request.listing != listing or exchange_request.sender != request.user:
        return redirect('home')
    if request.method == 'POST':
        exchange_request.delete()
        messages.success(request, 'Exchange request cancelled successfully.')
        return redirect('listing_detail', pk=pk)
    return render(request, 'exchange/cancel_exchange_request.html', {'exchange_request': exchange_request})

@login_required
def delete_exchange_request(request, pk, request_id):
    listing = get_object_or_404(Listing, pk=pk)
    exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)
    if exchange_request.listing != listing or exchange_request.sender != request.user:
        return redirect('home')
    if request.method == 'POST':
        exchange_request.delete()
        messages.success(request, 'Exchange request deleted successfully.')
        return redirect('manage_exchange_requests', pk=pk)
    return render(request, 'exchange/delete_exchange_request.html', {'exchange_request': exchange_request})
