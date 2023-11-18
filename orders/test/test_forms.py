from django.test import TestCase
from orders.forms import OrderCreateForm


class OrderCreateFormTest(TestCase):
    def test_order_create_form_fields(self):
        form = OrderCreateForm()
        expected_fields = ["full_name", "email", "phone", "address"]
        form_fields = list(form.fields.keys())
        self.assertEqual(form_fields, expected_fields)

    def test_order_create_form_valid_data(self):
        form = OrderCreateForm(data={
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "1234567890",
            "address": "123 Main St"
        })
        self.assertTrue(form.is_valid())

    def test_order_create_form_empty_data(self):
        form = OrderCreateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_order_create_form_missing_required_fields(self):
        form = OrderCreateForm(data={
            "full_name": "John Doe",
            "email": "",
            "phone": "",
            "address": ""
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
