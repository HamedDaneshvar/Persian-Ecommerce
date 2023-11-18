from django import forms
from orders.models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ["full_name", "email", "phone", "address",]
