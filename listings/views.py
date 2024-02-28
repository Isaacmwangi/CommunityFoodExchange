# listings/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Listing
from .forms import ListingForm
from django.utils import timezone


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
    return render(request, 'listings/listing_detail.html', {'listing': listing})

@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        listing.delete()
        return redirect('home')
    return render(request, 'listings/listing_confirm_delete.html', {'listing': listing})
