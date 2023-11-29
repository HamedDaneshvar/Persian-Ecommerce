from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from payments.admin import PaymentAdmin
from payments.models import Payment


class PaymentAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.request_factory = RequestFactory()

    def test_payment_admin_list_display(self):
        payment_admin = PaymentAdmin(Payment, self.site)
        expected_list_display = ["name", "types", "available", "create_at", "updated_at"]
        self.assertEqual(payment_admin.list_display, expected_list_display)

    def test_payment_admin_list_filter(self):
        payment_admin = PaymentAdmin(Payment, self.site)
        expected_list_filter = ["available", "create_at", "updated_at"]
        self.assertEqual(payment_admin.list_filter, expected_list_filter)

    def test_payment_admin_list_view(self):
        payment = Payment.objects.create(
            name="Test Payment",
            merchant="12345678-1234-1234-1234-123456789012",
            types="zarinpal",
            available=True
        )
        request = self.request_factory.get("/admin/myapp/payment/")
        payment_admin = PaymentAdmin(Payment, self.site)
        queryset = payment_admin.get_queryset(request)
        self.assertIn(payment, queryset)
