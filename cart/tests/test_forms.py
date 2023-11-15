from django.test import TestCase
from cart.forms import CartAddProductForm


class CartAddProductFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            'quantity': 2,
            'override': False
        }
        form = CartAddProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_quantity(self):
        form_data = {
            'quantity': 0,  # Invalid quantity
            'override': False
        }
        form = CartAddProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('quantity', form.errors)

    def test_negative_quantity_override(self):
        form_data = {
            'quantity': -2,  # Negative quantity
            'override': True  # Override enabled
        }
        form = CartAddProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('quantity', form.errors)

    def test_missing_quantity_override(self):
        form_data = {
            'quantity': 2,
            # 'override' field missing
        }
        form = CartAddProductForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)
        self.assertNotIn('override', form.errors)

    def test_form_label(self):
        form = CartAddProductForm()
        self.assertEqual(form.fields['quantity'].label, '')

    def test_form_widget_attrs(self):
        form = CartAddProductForm()
        self.assertEqual(form.fields['quantity'].widget.attrs['class'],
                         'form-control cart-quantity-input')
        self.assertEqual(form.fields['quantity'].widget.attrs['step'], '1')

    def test_override_widget_attrs(self):
        form = CartAddProductForm()
        self.assertEqual(form.fields['override'].widget.input_type, 'hidden')

    def test_override_default_value(self):
        form = CartAddProductForm()
        self.assertFalse(form.fields['override'].initial)

    def test_override_required(self):
        form_data = {
            'quantity': 2,
            'override': None  # Missing override value
        }
        form = CartAddProductForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)
        self.assertNotIn('override', form.errors)

    def test_quantity_min_value(self):
        form_data = {
            'quantity': 0,  # Minimum value is 1
            'override': False
        }
        form = CartAddProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('quantity', form.errors)
