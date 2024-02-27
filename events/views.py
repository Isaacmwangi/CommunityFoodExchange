from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm

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

def upcoming_events(request):
    events = Event.objects.filter(date__gte=date.today())
    return render(request, 'events/upcoming_events.html', {'events': events})
