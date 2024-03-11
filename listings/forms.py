# listings/forms.py
from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    quantity = forms.CharField(label='Quantity', max_length=100, help_text='Enter quantity description (e.g., 2 kgs, 500 grams, 1 sack)')
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}))
    preferred_exchange_method = forms.CharField(label='Preferred Exchange Method', max_length=200, help_text='Enter preferred exchange method')

    class Meta:
        model = Listing
        fields = ['item_name', 'description', 'quantity', 'expiration_date', 'preferred_exchange_method', 'image']
