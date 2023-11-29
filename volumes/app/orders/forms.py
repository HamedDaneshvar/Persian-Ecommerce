from django import forms
from orders.models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        """
        Form class for creating Order objects.

        This form is used to create new Order objects based on the provided
        fields.

        Attributes:
            - model (Order): The model associated with the form.
            - fields (list): The fields to include in the form.
        """
        model = Order
        fields = ["full_name", "email", "phone", "address",]
