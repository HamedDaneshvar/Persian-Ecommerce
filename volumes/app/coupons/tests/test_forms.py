from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from coupons.models import Coupon
from coupons.forms import CouponApplyForm


class CouponApplyFormTest(TestCase):
    def setUp(self):
        now = timezone.localtime(timezone.now())
        valid_from = now
        valid_to = now + timedelta(days=30)
        self.coupon = Coupon.objects.create(
            code="TESTCODE",
            valid_from=valid_from,
            valid_to=valid_to,
            discount=10,
            active=True
        )

    def test_valid_coupon_code(self):
        form = CouponApplyForm(data={'code': self.coupon.code})
        self.assertTrue(form.is_valid())

    def test_invalid_coupon_code(self):
        form = CouponApplyForm(data={'code': 'INVALIDCODE'})
        self.assertTrue(form.is_valid())
        self.assertNotIn('code', form.errors)

    def test_blank_coupon_code(self):
        form = CouponApplyForm(data={'code': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('code', form.errors)
