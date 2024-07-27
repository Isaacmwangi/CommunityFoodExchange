# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from ratings_reviews.forms import ReviewForm  # Import ReviewForm from ratings_reviews.forms
from .models import Profile
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator

class UsernameUpdateForm(UserChangeForm):
    username = forms.CharField(
        label='New Username',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.',
                code='invalid_username',
            ),
        ],
    )
 

class CustomPasswordResetForm(forms.Form):
    email_or_username = forms.CharField(label='Email or Username', max_length=254)

   
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'dietary_preferences', 'food_allergies', 'email', 'first_name', 'last_name', 'mobile_number']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        validators=[EmailValidator()],
        required=True,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']