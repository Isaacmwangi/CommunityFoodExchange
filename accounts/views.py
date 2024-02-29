# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth import logout  
from listings.models import Listing  
from exchange.models import ExchangeRequest 
from messaging.models import Message 
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        """If the form is valid, redirect to the home page."""
        login(self.request, form.get_user())
        return redirect('home')  # Redirect to the home page

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
    except Profile.DoesNotExist:
        return redirect('profile_create')  # Redirect to profile creation if profile doesn't exist
    return render(request, 'accounts/profile.html', {'profile': profile})

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
    upcoming_events = []  # Assuming you have logic to retrieve upcoming events
    unread_messages_count = Message.objects.filter(conversation__participants=request.user, is_read=False).count()
    exchange_requests = ExchangeRequest.objects.filter(receiver=request.user)  # Fetch exchange requests
    return render(request, 'accounts/home.html', {'featured_listings': featured_listings, 'upcoming_events': upcoming_events, 'unread_messages_count': unread_messages_count, 'exchange_requests': exchange_requests})



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
