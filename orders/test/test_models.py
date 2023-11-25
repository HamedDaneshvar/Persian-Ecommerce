from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from coupons.models import Coupon
from transportation.models import Transport
from shop.models import Category, Product
from orders.models import Order, OrderItem


User = get_user_model()


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="johndoe@example.com",
            password="dqlj3r23u9f",
            full_name="John Doe")
        self.coupon = Coupon.objects.create(
            code="SUMMER10",
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=1),
            discount=10,
            active=True
        )
        self.transport = Transport.objects.create(
            name="Express Shipping",
            delivery="Fast delivery within 2-3 business days",
            price=5.99,
            activate=True
        )
        self.order = Order.objects.create(
            user=self.user,
            coupon=self.coupon,
            transport=self.transport,
            full_name="John Doe",
            email="johndoe@example.com",
            phone="1234567890",
            address="123 ABC Street",
            paid=False,
            discount=10,
            transaction_id=12345,
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            slug='test-product',
            price=19.99,
            available=True
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=19.99,
            quantity=2
        )

    def test_get_total_cost_before_discount(self):
        total_cost = self.order_item.price * self.order_item.quantity
        self.assertIsInstance(self.order.get_total_cost_before_discount(),
                              Decimal)
        self.assertEqual(float(self.order.get_total_cost_before_discount()),
                         total_cost)

    def test_get_discount(self):
        discount_amount = self.order.get_total_cost_before_discount() * \
            (self.order.discount / Decimal(100))
        self.assertEqual(self.order.get_discount(), discount_amount)
        self.assertIsInstance(self.order.get_discount(), Decimal)

    def test_get_total_cost(self):
        transport_price = self.transport.price
        total_cost = (float(self.order_item.price) * self.order_item.quantity)\
            + transport_price
        expected_cost = total_cost - float(self.order.get_discount())
        self.assertEqual(float(self.order.get_total_cost()), expected_cost)
        self.assertIsInstance(self.order.get_total_cost(), str)

    def test_order_str(self):
        expected_str = f"Order {self.order.id}"
        self.assertEqual(str(self.order), expected_str)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="johndoe@example.com",
            password="dqlj3r23u9f",
            full_name="John Doe")
        self.order = Order.objects.create(
            user=self.user,
            full_name="John Doe",
            email="johndoe@example.com",
            phone="1234567890",
            address="123 ABC Street",
            paid=False,
            discount=10,
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            slug='test-product',
            price=19.99,
            available=True
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=19.99,
            quantity=2
        )

    def test_get_cost(self):
        cost = self.order_item.price * self.order_item.quantity
        self.assertEqual(self.order_item.get_cost(), cost)
