from django.test import TestCase
from transportation.models import Transport


class TransportModelTestCase(TestCase):
    def setUp(self):
        self.transport = Transport.objects.create(
            name="Express Shipping",
            delivery="Fast delivery within 2-3 business days",
            price=10.99,
            activate=True
        )

    def test_transport_str(self):
        self.assertEqual(str(self.transport), "Express Shipping: Fast delivery"
                         " within 2-3 business days")

    def test_transport_attributes(self):
        self.assertEqual(self.transport.name, "Express Shipping")
        self.assertEqual(self.transport.delivery, "Fast delivery within 2-3 "
                         "business days")
        self.assertEqual(self.transport.price, 10.99)
        self.assertTrue(self.transport.activate)

    def test_transport_activation(self):
        self.assertTrue(self.transport.activate)

        self.transport.activate = False
        self.assertFalse(self.transport.activate)

        self.transport.activate = True
        self.assertTrue(self.transport.activate)
