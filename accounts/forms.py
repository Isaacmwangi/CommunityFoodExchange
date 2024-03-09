# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ratings_reviews.forms import ReviewForm  # Import ReviewForm from ratings_reviews.forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'dietary_preferences', 'food_allergies', 'email', 'first_name', 'last_name', 'mobile_number']
