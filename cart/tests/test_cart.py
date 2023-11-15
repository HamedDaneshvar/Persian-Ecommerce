from decimal import Decimal
from django.utils import timezone
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from shop.models import Category, Product
from coupons.models import Coupon
from cart.cart import Cart


class CartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()
        self.cart = Cart(self.request)
        self.category = Category.objects.create(name='Test Category',
                                                slug='test-category')
        self.product1 = Product.objects.create(
            name='Product 1',
            category=self.category,
            slug='product-1',
            price=10,
            available=True
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            category=self.category,
            slug='product-2',
            price=20,
            available=True
        )

    def test_add_product_to_cart(self):
        self.cart.add(self.product1, quantity=2)
        self.assertEqual(len(self.cart), 2)

    def test_update_product_quantity(self):
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product1, quantity=3, override_quantity=True)
        self.assertEqual(len(self.cart), 3)

    def test_remove_product_from_cart(self):
        self.cart.add(self.product1, quantity=2)
        self.cart.remove(self.product1)
        self.assertEqual(len(self.cart), 0)

    def test_clear_cart(self):
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product2, quantity=1)
        self.cart.clear()
        self.assertEqual(len(self.cart), 0)

    def test_get_total_price(self):
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product2, quantity=1)
        expected_total_price = Decimal(10 * 2) + Decimal(20 * 1)
        self.assertEqual(self.cart.get_total_price(), expected_total_price)

    def test_apply_coupon(self):
        coupon = Coupon.objects.create(
            code="TESTCOUPON",
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=7),
            discount=25,
            active=True
        )
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product2, quantity=1)
        self.cart.coupon_id = coupon.id
        expected_discount = (Decimal(25) / Decimal(100)) * \
            self.cart.get_total_price()
        expected_total_price = self.cart.get_total_price() - expected_discount
        self.assertEqual(self.cart.get_discount(), expected_discount)
        self.assertEqual(self.cart.get_total_price_after_discount(),
                         expected_total_price)

    def test_get_coupon_when_not_applied(self):
        self.assertIsNone(self.cart.coupon)

    def test_get_coupon_when_not_exists(self):
        self.cart.coupon_id = 999
        self.assertIsNone(self.cart.coupon)

    def test_iterate_over_cart_items(self):
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product2, quantity=1)
        items = list(self.cart)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["product"], self.product1)
        self.assertEqual(items[1]["product"], self.product2)

    def test_get_total_price_after_discount_when_no_coupon(self):
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product2, quantity=1)
        self.assertEqual(self.cart.get_total_price_after_discount(),
                         self.cart.get_total_price())

    def test_get_total_price_after_discount_when_coupon_does_not_exist(self):
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product2, quantity=1)
        self.cart.coupon_id = 999
        self.assertEqual(self.cart.get_total_price_after_discount(),
                         self.cart.get_total_price())
