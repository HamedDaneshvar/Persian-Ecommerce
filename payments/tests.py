from django.test import TestCase
from django.core.exceptions import ValidationError
from payments.models import Payment


class PaymentModelTestCase(TestCase):
    def create_payment(self):
        payment = Payment.objects.create(
            name="Test Payment",
            merchant="12345678-1234-1234-1234-123456789012",
            types="zarinpal",
            available=True
        )
        return payment

    def test_payment_creation(self):
        self.payment = self.create_payment()
        self.assertIsInstance(self.payment, Payment)
        self.assertEqual(self.payment.name, "Test Payment")
        self.assertEqual(self.payment.merchant,
                         "12345678-1234-1234-1234-123456789012")
        self.assertEqual(self.payment.types, "zarinpal")
        self.assertTrue(self.payment.available)

    def test_payment_str_representation(self):
        self.payment = self.create_payment()
        expected_str = "Test Payment: Zarinpal Payment Gateway"
        self.assertEqual(str(self.payment), expected_str)

    def test_payment_save_invalid_merchant(self):
        self.payment = self.create_payment()
        invalid_merchant = "invalid_merchant_id"
        payment = Payment(
            name="Invalid Payment",
            merchant=invalid_merchant,
            types="zarinpal",
            available=True
        )
        with self.assertRaises(ValueError):
            payment.save()

    def test_payment_save_valid_merchant(self):
        valid_merchant = "87654321-4321-4321-4321-210987654321"
        payment = Payment(
            name="Valid Payment",
            merchant=valid_merchant,
            types="zarinpal",
            available=True
        )
        payment.save()
        self.assertEqual(payment.merchant, valid_merchant)

    def test_payment_verbose_names(self):
        self.assertEqual(Payment._meta.verbose_name, "Payment")
        self.assertEqual(Payment._meta.verbose_name_plural, "Payments")

    def test_payment_invalid_type(self):
        invalid_type = "invalid_type"
        with self.assertRaises(ValidationError):
            payment = Payment(
                name="Invalid Payment",
                merchant="12345678-1234-1234-1234-123456789012",
                types=invalid_type,
                available=True
            )
            payment.full_clean()
