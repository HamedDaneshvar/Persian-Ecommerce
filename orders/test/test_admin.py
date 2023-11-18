from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, RequestFactory
from orders.admin import OrderAdmin, OrderItemInline
from orders.models import Order, OrderItem


class OrderAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()
        self.order_admin = OrderAdmin(Order, self.site)

    def test_order_admin_list_display(self):
        self.assertEqual(
            self.order_admin.list_display,
            ["full_name", "email", "phone", "address", "transport",
             "get_total_cost", "fee", "paid", "create_at", "updated_at"]
        )

    def test_order_admin_list_filter(self):
        self.assertEqual(
            self.order_admin.list_filter,
            ["paid", "create_at", "updated_at"]
        )

    def test_order_admin_inlines(self):
        self.assertEqual(
            self.order_admin.inlines,
            [OrderItemInline]
        )

    def test_order_item_inline_model(self):
        order_item_inline = OrderItemInline(Order, self.site)
        self.assertEqual(
            order_item_inline.model,
            OrderItem
        )

    def test_order_item_inline_raw_id_fields(self):
        order_item_inline = OrderItemInline(Order, self.site)
        self.assertEqual(
            order_item_inline.raw_id_fields,
            ["product"]
        )

    def test_order_admin_register(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="dqlj3r23u9f",
            full_name="John Doe")

        request = self.factory.get(reverse("admin:orders_order_changelist"))
        request.user = user
        changelist = self.order_admin.get_changelist_instance(request)
        self.assertIsNotNone(changelist)
