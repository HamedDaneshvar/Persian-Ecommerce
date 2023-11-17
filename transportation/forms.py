from django import forms
from .models import Transport


class TransportChoiceForm(forms.Form):
    """
    Form for selecting a transport choice.

    This form allows users to select a transport choice from the available
    options. It uses the `ModelChoiceField` to display a list of transports
    that are currently activated.

    Attributes:
        - transport (ModelChoiceField): The field representing the transport
          choice.
        - queryset (QuerySet): The queryset used to populate the transport
          choices.
        - widget (RadioSelect): The widget used to render the transport
          choices as radio buttons.
        - label (str): The label for the transport choice field.

    """
    transport = forms.ModelChoiceField(
        queryset=Transport.objects.filter(activate=True),
        widget=forms.RadioSelect,
        label=""
    )
