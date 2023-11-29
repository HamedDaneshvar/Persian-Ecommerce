from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from coupons.models import Coupon


class CouponModelTestCase(TestCase):
    def setUp(self):
        self.coupon = Coupon.objects.create(
            code='TESTCOUPON',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=1),
            discount=10,
            active=True
        )

    def test_coupon_creation(self):
        # Test that a coupon is created successfully
        self.assertEqual(self.coupon.code, 'TESTCOUPON')
        self.assertEqual(self.coupon.discount, 10)
        self.assertTrue(self.coupon.active)

    def test_coupon_str_representation(self):
        # Test the __str__ method of the coupon model
        self.assertEqual(str(self.coupon), 'TESTCOUPON')

    def test_coupon_validity(self):
        # Test the validity of the coupon
        self.assertTrue(self.coupon.is_valid())
        self.coupon.valid_to = timezone.now() - timezone.timedelta(days=1)
        self.assertFalse(self.coupon.is_valid())

    def test_coupon_discount_range(self):
        # Test the discount range of the coupon
        self.assertEqual(self.coupon.discount, 10)
        self.coupon.discount = 101
        with self.assertRaises(ValidationError):
            self.coupon.save()
        self.coupon.discount = -1
        with self.assertRaises(ValidationError):
            self.coupon.save()

    def test_coupon_code_uniqueness(self):
        # Test the uniqueness of coupon codes
        with self.assertRaises(Exception):
            Coupon.objects.create(
                code='TESTCOUPON',
                valid_from=timezone.now(),
                valid_to=timezone.now(),
                discount=10,
                active=True
            )
