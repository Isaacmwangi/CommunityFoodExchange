# exchange/forms.py

from django import forms
from .models import ExchangeRequest

class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = ['message']