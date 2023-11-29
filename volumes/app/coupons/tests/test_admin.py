from datetime import timedelta
from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from coupons.admin import CouponAdmin
from coupons.models import Coupon


class CouponAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()
        self.admin = CouponAdmin(Coupon, self.site)

    def test_list_display(self):
        # Test that the list_display attributes are set correctly
        expected_list_display = ["code", "valid_from", "valid_to",
                                 "discount", "active"]
        self.assertEqual(self.admin.list_display, expected_list_display)

    def test_list_filter(self):
        # Test that the list_filter attributes are set correctly
        expected_list_filter = ["active", "valid_from", "valid_to"]
        self.assertEqual(self.admin.list_filter, expected_list_filter)

    def test_search_fields(self):
        # Test that the search_fields attribute is set correctly
        expected_search_fields = ["code"]
        self.assertEqual(self.admin.search_fields, expected_search_fields)

    def test_coupon_admin_coverage(self):
        # Create a sample coupon object
        now = timezone.localtime(timezone.now())
        valid_from = now
        valid_to = now + timedelta(days=30)
        coupon = Coupon.objects.create(
            code="TESTCODE",
            valid_from=valid_from,
            valid_to=valid_to,
            discount=10,
            active=True)

        # Create a test user with necessary permissions
        User = get_user_model()
        user = User.objects.create_user(
            email="admin@example.com",
            password="dqlj3r23u9f",
            full_name="John Doe")
        perm_view = Permission.objects.get(codename="view_coupon")
        perm_add = Permission.objects.get(codename="add_coupon")
        user.user_permissions.add(perm_view, perm_add)

        # Authenticate the user
        self.client.login(email="testuser", password="dqlj3r23u9f")

        # Create a request
        request = self.factory.get("/admin/coupons/coupon/")
        request.user = user

        # Test the get_queryset method
        queryset = self.admin.get_queryset(request)
        self.assertIn(coupon, queryset)

        # Test the changelist_view method
        response = self.admin.changelist_view(request)
        self.assertEqual(response.status_code, 200)

        # Test the add_view method
        response = self.admin.add_view(request)
        self.assertEqual(response.status_code, 200)

        # Test the change_view method
        response = self.admin.change_view(request, str(coupon.id))
        self.assertEqual(response.status_code, 200)

        # Test the history_view method
        response = self.admin.history_view(request, str(coupon.id))
        self.assertEqual(response.status_code, 200)
