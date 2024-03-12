# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth import logout  
from listings.models import Listing  
from exchange.models import ExchangeRequest 
from messaging.models import Message 
from django.db.models import Max
from events.models import Event  
from django.urls import reverse_lazy
from ratings_reviews.models import Review 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm  # Set the form class explicitly

    def form_invalid(self, form):
        """If the form is invalid, render the login form with error messages."""
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        """Redirect to the home page after successful login."""
        return reverse_lazy('home')


class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful signup and login
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
        user_reviews = Review.objects.filter(reviewed_user=request.user)
    except Profile.DoesNotExist:
        return redirect('profile_create')  # Redirect to profile creation if profile doesn't exist
    return render(request, 'accounts/profile.html', {'profile': profile, 'user_reviews': user_reviews})


@login_required
def profile_create(request):
    try:
        profile = Profile.objects.get(user=request.user)
        return redirect('profile_update')  # Redirect to profile update if profile already exists
    except Profile.DoesNotExist:
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('home')
        else:
            form = ProfileForm()
        return render(request, 'accounts/profile_create.html', {'form': form})

@login_required
def profile_update(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('profile_create')  # Redirect to profile creation if profile doesn't exist
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_update.html', {'form': form})

def user_logout(request):  # Define a user_logout view
    logout(request)  # Call the logout function
    return redirect('home')  # Redirect to the home page after logout


@login_required
def home(request):
    featured_listings = Listing.objects.all()  # Fetch all listings
    upcoming_events = Event.objects.all().order_by('date')  # Fetch all upcoming events
    exchange_requests = ExchangeRequest.objects.filter(receiver=request.user)  # Fetch exchange requests
    action_message = request.session.pop('action_message', None)  # Get action message from session
    
    # Fetch and count unread messages for the current user
    unread_messages_count = Message.objects.filter(conversation__participants=request.user, is_read=False).count()
    
    latest_conversation = request.user.conversations.annotate(latest_message_timestamp=Max('messages__timestamp')).order_by('-latest_message_timestamp').first()
    latest_conversation_id = latest_conversation.id if latest_conversation else None
    
    # Fetch all user reviews and order them by the creation date in descending order
    user_reviews = Review.objects.all().order_by('-created_at')
    
    return render(request, 'accounts/home.html', {
        'featured_listings': featured_listings,
        'upcoming_events': upcoming_events,  # Include upcoming_events in the context
        'unread_messages_count': unread_messages_count,
        'exchange_requests': exchange_requests,
        'action_message': action_message,
        'latest_conversation_id': latest_conversation_id,
        'user_reviews': user_reviews,  # Pass user_reviews to the template
    })



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)