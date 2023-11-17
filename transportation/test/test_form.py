from django.test import TestCase
from transportation.models import Transport
from transportation.forms import TransportChoiceForm


class TransportChoiceFormTest(TestCase):
    def setUp(self):
        self.transport1 = Transport.objects.create(
            name="Express Shipping",
            delivery="Fast delivery within 2-3 business days",
            price=10.99,
            activate=True
        )
        self.transport2 = Transport.objects.create(
            name="Standard Shipping",
            delivery="Delivery within 5-7 business days",
            price=5.99,
            activate=True
        )

    def test_transport_choice_form(self):
        form_data = {
            'transport': self.transport1.pk
        }
        form = TransportChoiceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_transport_choice_form_invalid(self):
        form_data = {
            'transport': None
        }
        form = TransportChoiceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('transport', form.errors)
