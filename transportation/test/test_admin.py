from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase, RequestFactory
from transportation.models import Transport
from transportation.admin import TransportAdmin


class TransportAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_site = admin.AdminSite()
        self.transport = Transport.objects.create(
            name="Express Shipping",
            delivery="Fast delivery within 2-3 business days",
            price=10.99,
            activate=True
        )
        self.transport_admin = TransportAdmin(Transport, self.admin_site)

    def test_list_display(self):
        expected_list_display = ["name", "delivery", "price", "activate"]
        self.assertEqual(self.transport_admin.list_display,
                         expected_list_display)

    def test_list_editable(self):
        expected_list_editable = ["price", "activate"]
        self.assertEqual(self.transport_admin.list_editable,
                         expected_list_editable)

    def test_transport_admin_changelist(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="admin@example.com",
            password="dqlj3r23u9f",
            full_name="John Doe")

        self.client.login(email="testuser", password="dqlj3r23u9f")

        request = self.factory.get("/admin/")
        request.user = user
        changelist = self.transport_admin.get_changelist_instance(request)
        self.assertIsNotNone(changelist)

    def test_transport_admin_save_model(self):
        request = self.factory.post("/admin/")
        self.transport_admin.save_model(request, self.transport,
                                        form=None, change=None)
        self.transport.refresh_from_db()
        self.assertIsNotNone(self.transport.pk)
