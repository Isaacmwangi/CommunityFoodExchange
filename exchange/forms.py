# exchange/forms.py
from django import forms
from .models import ExchangeRequest

class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Enter your message here...'}),
        }

class CancelExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = ['reason_for_cancellation']
