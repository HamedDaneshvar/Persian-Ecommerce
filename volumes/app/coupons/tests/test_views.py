from datetime import timedelta
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from django.utils import timezone
from coupons.models import Coupon
from coupons.views import coupon_apply


class CouponApplyViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse("coupons:apply")
        self.session_middleware = SessionMiddleware()
        now = timezone.localtime(timezone.now())
        valid_from = now
        valid_to = now + timedelta(days=30)
        self.valid_coupon = Coupon.objects.create(
            code="TESTCODE",
            valid_from=valid_from,
            valid_to=valid_to,
            discount=10,
            active=True
        )
        self.invalid_coupon = Coupon.objects.create(
            code="INVALIDCODE",
            valid_from=now - timedelta(days=30),
            valid_to=now - timedelta(days=1),
            discount=10,
            active=True
        )

    def test_apply_valid_coupon(self):
        data = {"code": self.valid_coupon.code}
        request = self.factory.post(self.url, data)
        self.session_middleware.process_request(request)
        request.session.save()
        response = coupon_apply(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.session["coupon_id"], self.valid_coupon.id)
        self.assertEqual(request.session["coupon_code"],
                         self.valid_coupon.code)

    def test_apply_invalid_coupon(self):
        data = {"code": self.invalid_coupon.code}
        request = self.factory.post(self.url, data)
        self.session_middleware.process_request(request)
        request.session.save()
        response = coupon_apply(request)
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(request.session["coupon_id"])
        self.assertEqual(request.session["coupon_code"],
                         self.invalid_coupon.code)

    def test_apply_blank_coupon(self):
        data = {"code": ""}
        request = self.factory.post(self.url, data)
        self.session_middleware.process_request(request)
        request.session.save()
        response = coupon_apply(request)
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(request.session["coupon_id"])
        self.assertNotIn("coupon_code", request.session)

    def test_get_request(self):
        request = self.factory.get(self.url)
        self.session_middleware.process_request(request)
        request.session.save()
        response = coupon_apply(request)
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(request.session["coupon_id"])
        self.assertNotIn("coupon_code", request.session)
