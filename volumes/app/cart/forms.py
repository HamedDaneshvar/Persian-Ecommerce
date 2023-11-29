from django import forms


class CartAddProductForm(forms.Form):
    """
    Form used for adding a product to the cart.

    This form provides fields for specifying the quantity of the product to
    be added, as well as an optional field to override the quantity if needed.
    """
    quantity = forms.IntegerField(
        initial=1,
        min_value=1,
        label="",
        widget=forms.widgets.NumberInput(
            attrs={
                "class": "form-control cart-quantity-input",
                "step": "1", }
        ),
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
