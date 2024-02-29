# listings/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from .models import Listing
from .forms import ListingForm
from django.http import HttpResponseRedirect
from exchange.models import ExchangeRequest
from messaging.models import Conversation 

class ListingCreateView(CreateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'
    success_url = reverse_lazy('home')
    


class ListingUpdateView(UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'
    success_url = reverse_lazy('home')

class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'

class ListingDeleteView(DeleteView):
    model = Listing
    template_name = 'listings/listing_confirm_delete.html'
    success_url = reverse_lazy('home')

@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('home')
    else:
        form = ListingForm()
    return render(request, 'listings/listing_form.html', {'form': form})

@login_required
def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/listing_form.html', {'form': form, 'listing': listing})

@login_required
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    exchange_requests = ExchangeRequest.objects.filter(listing=listing)
    is_owner = listing.user == request.user
    can_request = not is_owner  # User cannot request their own listing

    # Check if the current user has already sent a request for the listing
    has_sent_request = False
    if request.user.is_authenticated:
        has_sent_request = exchange_requests.filter(sender=request.user).exists()

    if request.method == 'POST':
        if 'delete_listing' in request.POST:
            return render(request, 'listings/listing_confirm_delete.html', {'listing': listing})
        elif 'send_request' in request.POST:
            # Check if the user has already sent a request for this listing
            if has_sent_request:
                messages.error(request, 'You have already sent a request for this item.')
            elif listing.user == request.user:
                messages.error(request, 'You cannot send a request to your own post.')
            else:
                # Create a new exchange request
                ExchangeRequest.objects.create(listing=listing, sender=request.user)
                messages.success(request, 'Exchange request sent successfully.')
            return redirect('listing_detail', pk=pk)

    return render(request, 'listings/listing_detail.html', {'listing': listing, 'exchange_requests': exchange_requests, 'is_owner': is_owner, 'can_request': can_request, 'has_sent_request': has_sent_request})




class ListingDeleteView(DeleteView):
    model = Listing
    template_name = 'listings/listing_confirm_delete.html'
    success_url = reverse_lazy('home')

    #method to handle POST requests for deletion confirmation
    def post(self, request, *args, **kwargs):
        if "confirm_delete" in request.POST:
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.success_url)

@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted successfully.')
        return redirect('home')
    return render(request, 'listings/listing_confirm_delete.html', {'listing': listing})