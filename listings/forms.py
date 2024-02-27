# listings/forms.py

from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['item_name', 'description', 'quantity', 'expiration_date']
