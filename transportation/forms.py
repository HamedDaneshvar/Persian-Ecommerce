from django import forms
from .models import Transport

class TransportChoiceForm(forms.Form):
	transport = forms.ModelChoiceField(queryset=Transport.objects
													.filter(activate=True),
													widget=forms.RadioSelect,
													label="")