from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.sessions.middleware import SessionMiddleware
from shop.models import Category, Product
from transportation.models import Transport
from coupons.models import Coupon
from cart.cart import Cart
from orders.models import OrderItem, Order
from orders.views import order_create, send_to_payment


class OrderCreateViewTest(TestCase):
    def setUp(self):
        self.user = self.create_user()
        self.category = self.create_category()
        self.product1 = self.create_product('project1', 10)
        self.product2 = self.create_product('project2', 20)
        self.transport = self.create_transport()

        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.session_middleware = SessionMiddleware()
        self.session_middleware.process_request(self.request)
        self.request.session.save()
        self.client = Client()

        self.cart = Cart(self.request)
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product2, quantity=1)

        self.order_form_data = {
            "order_form-full_name": "John Doe",
            "order_form-email": "test@example.com",
            "order_form-phone": "1234567890",
            "order_form-address": "Test Address",
        }
        self.transportation_form_data = {
            "transportation_form-transport": self.transport.id,
        }

    def create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass',
            full_name='John Doe'
        )
        return user

    def create_category(self):
        category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        return category

    def create_product(self, name, price):
        image = SimpleUploadedFile(
            name='test_image.jpg', content=b'',
            content_type='image/jpeg')
        product = Product.objects.create(
            name=f'{name}',
            category=self.category,
            slug=f'{name}',
            description='Test description',
            price=price,
            image=image,
            available=True
        )
        return product

    def create_transport(self):
        transport = Transport.objects.create(
            name="Express Shipping",
            delivery="Fast delivery within 2-3 business days",
            price=10.99,
            activate=True
        )
        return transport

    def create_coupon(self, discount):
        coupon = Coupon.objects.create(
            code="TESTCODE",
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=30),
            discount=discount,
            active=True
        )
        return coupon

    def test_order_create_anonymous_user_redirects_to_login(self):
        url = reverse('accounts:login') + "?next=" + \
            reverse("orders:order_create")
        response = self.client.get(reverse("orders:order_create"))
        self.assertRedirects(response, url)

    def test_order_create_valid_form_creates_order_and_items(self):
        self.request = self.factory.post(reverse("orders:order_create"), {
            **self.order_form_data,
            **self.transportation_form_data,
        })
        self.request.user = self.user
        self.session_middleware.process_request(self.request)
        self.request.session.save()
        self.coupon = self.create_coupon(discount=10)
        self.request.session['coupon_id'] = self.coupon.id
        self.request.session['coupon_code'] = self.coupon.code
        self.cart = Cart(self.request)
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product2, quantity=1)
        response = order_create(self.request)
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, "payments/payment-success.html")
        self.assertEqual(OrderItem.objects.count(), 2)

    def test_order_create_zero_cost_order_redirects_to_payment_success(self):
        self.request = self.factory.post(reverse("orders:order_create"), {
            **self.order_form_data,
            **self.transportation_form_data,
        })
        self.request.user = self.user
        self.session_middleware.process_request(self.request)
        self.request.session.save()
        self.coupon = self.create_coupon(discount=100)
        self.request.session['coupon_id'] = self.coupon.id
        self.request.session['coupon_code'] = self.coupon.code
        self.cart = Cart(self.request)
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product2, quantity=1)
        response = order_create(self.request)

        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, "payments/payment-success.html")

    def test_order_create_invalid_form_returns_form_errors(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("orders:order_create"), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/order/checkout.html")
        self.assertContains(response, "This field is required.", html=False)

    def test_order_create_get_request_returns_checkout_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("orders:order_create"))
        self.assertEqual(response.status_code, 200)

    def test_order_create_authenticated_user_saves_order_with_user(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("orders:order_create"), {
            **self.order_form_data,
            **self.transportation_form_data,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("payments:request"))


class OrderListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user()
        self.category = self.create_category()
        self.product = self.create_product("product1", 10)
        self.transport = self.create_transport()
        self.orders = self.create_orders()

    def create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass',
            full_name='John Doe'
        )
        return user

    def create_category(self):
        category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        return category

    def create_product(self, name, price):
        image = SimpleUploadedFile(
            name='test_image.jpg', content=b'',
            content_type='image/jpeg')
        product = Product.objects.create(
            name=f'{name}',
            category=self.category,
            slug=f'{name}',
            description='Test description',
            price=price,
            image=image,
            available=True
        )
        return product

    def create_transport(self):
        transport = Transport.objects.create(
            name="Express Shipping",
            delivery="Fast delivery within 2-3 business days",
            price=10.99,
            activate=True
        )
        return transport

    def create_orders(self):
        orders = []
        for i in range(3):
            order = Order.objects.create(
                user=self.user,
                full_name="John Doe",
                email="test@example.com",
                phone="1234567890",
                address="Test Address",
                transport=self.transport,
            )
            OrderItem.objects.create(
                order=order,
                product=self.product,
                price=10,
                quantity=1)
            orders.append(order)
        return orders

    def test_orders_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('orders:orders_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 3)
        self.assertTemplateUsed(response, 'orders/order/my-orders.html')


class OrderDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user()
        self.category = self.create_category()
        self.product = self.create_product("Product", 10)
        self.transport = self.create_transport()
        self.order = self.create_order()

    def create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass',
            full_name='John Doe'
        )
        return user

    def create_category(self):
        category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        return category

    def create_product(self, name, price):
        image = SimpleUploadedFile(
            name='test_image.jpg', content=b'',
            content_type='image/jpeg')
        product = Product.objects.create(
            name=f'{name}',
            category=self.category,
            slug=f'{name}',
            description='Test description',
            price=price,
            image=image,
            available=True
        )
        return product

    def create_transport(self):
        transport = Transport.objects.create(
            name="Express Shipping",
            delivery="Fast delivery within 2-3 business days",
            price=10.99,
            activate=True
        )
        return transport

    def create_order(self):
        order = Order.objects.create(
            user=self.user,
            full_name="John Doe",
            email="test@example.com",
            phone="1234567890",
            address="Test Address",
            transport=self.transport)
        OrderItem.objects.create(
            order=order,
            product=self.product,
            price=10,
            quantity=1)
        return order

    def test_order_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('orders:order_detail',
                                           args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['order'], self.order)
        self.assertEqual(len(response.context['items']), 1)
        self.assertTemplateUsed(response, 'orders/order/detail.html')


class SendToPaymentViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.session_middleware = SessionMiddleware()
        self.user = self.create_user()
        self.category = self.create_category()
        self.product = self.create_product("Product", 10)
        self.transport = self.create_transport()
        self.order = self.create_order()

    def create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass',
            full_name='John Doe'
        )
        return user

    def create_category(self):
        category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        return category

    def create_product(self, name, price):
        image = SimpleUploadedFile(
            name='test_image.jpg', content=b'',
            content_type='image/jpeg')
        product = Product.objects.create(
            name=f'{name}',
            category=self.category,
            slug=f'{name}',
            description='Test description',
            price=price,
            image=image,
            available=True
        )
        return product

    def create_transport(self):
        transport = Transport.objects.create(
            name="Express Shipping",
            delivery="Fast delivery within 2-3 business days",
            price=10.99,
            activate=True
        )
        return transport

    def create_order(self):
        order = Order.objects.create(
            user=self.user,
            full_name="John Doe",
            email="test@example.com",
            phone="1234567890",
            address="Test Address",
            transport=self.transport)
        OrderItem.objects.create(
            order=order,
            product=self.product,
            price=10,
            quantity=1)
        return order

    def test_send_to_payment_authenticated_user(self):
        request = self.factory.get(reverse('orders:order_payment',
                                           args=[self.order.id]))
        request.user = self.user
        self.session_middleware.process_request(request)
        request.session.save()
        response = send_to_payment(request, self.order.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('payments:request'))
        self.assertEqual(request.session['amount'],
                         f'{float(self.order.get_total_cost()):.2f}')
        self.assertEqual(request.session['order_id'], self.order.id)

    def test_send_to_payment_order_not_found(self):
        request = self.factory.get(reverse('orders:order_payment', args=[999]))
        request.user = self.user
        response = send_to_payment(request, 999)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('orders:orders_list'))

    def test_send_to_payment_anonymous_user(self):
        request = self.factory.get(reverse('orders:order_payment',
                                           args=[self.order.id]))
        request.user = AnonymousUser()
        self.session_middleware.process_request(request)
        request.session.save()
        response = send_to_payment(request, self.order.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:login') + "?next=" +
                         reverse("orders:order_payment", args=[self.order.id]))
