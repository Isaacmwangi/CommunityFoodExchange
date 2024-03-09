# events/views.py

from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required
import datetime  

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  
            event.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    # Check if the current user is the organizer of the event or is a staff member
    if request.user == event.organizer or request.user.is_staff:
        event.delete()
    return HttpResponseRedirect(reverse('home'))

def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

def upcoming_events(request):
    # Retrieve upcoming events that are after the current date
    events = Event.objects.filter(date__gte=datetime.date.today()).order_by('date')
    return render(request, 'events/upcoming_events.html', {'events': events})

def event_rsvp(request, event_id):
    # Placeholder view function for event RSVP
    return HttpResponse("Event RSVP functionality coming soon!")
