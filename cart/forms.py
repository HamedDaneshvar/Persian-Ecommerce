from django import forms


class CartAddProductForm(forms.Form):
	quantity = forms.IntegerField(initial=1,
								  min_value=1,
								  label="",
								  widget=forms.widgets.NumberInput(
										attrs={
											"class": "form-control cart-quantity-input",
											"step": "1",
										}
								  ),
	)
	override = forms.BooleanField(required=False,
								  initial=False,
								  widget=forms.HiddenInput)