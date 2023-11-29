from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.sessions.middleware import SessionMiddleware
from shop.models import Category, Product
from coupons.models import Coupon
from cart.cart import Cart
from cart.views import cart_add, cart_remove


class CartViewsTestCase(TestCase):
    def setUp(self):
        self.user = self.create_user()
        self.category = self.create_category()
        self.product = self.create_product()
        self.coupon = self.create_coupon()

        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.session_middleware = SessionMiddleware()
        self.session_middleware.process_request(self.request)
        self.request.session.save()
        self.client = Client()

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

    def create_product(self):
        image = SimpleUploadedFile(
            name='test_image.jpg', content=b'',
            content_type='image/jpeg')
        product = Product.objects.create(
            name='Test Product',
            category=self.category,
            slug='test-product',
            description='Test description',
            price=10.00,
            image=image,
            available=True
        )
        return product

    def create_coupon(self):
        coupon = Coupon.objects.create(
            code='TESTCODE',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=7),
            discount=10,
            active=True
        )
        return coupon

    def test_cart_add(self):
        url = reverse('cart:cart_add', args=[self.product.id])
        self.request = self.factory.post(url, data={'quantity': 2,
                                                    'override': False})
        self.request.user = self.user
        self.session_middleware.process_request(self.request)
        self.request.session.save()
        response = cart_add(self.request, self.product.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart:cart_detail'))

    def test_cart_remove(self):
        url = reverse('cart:cart_remove', args=[self.product.id])
        self.request = self.factory.post(url)
        self.request.user = self.user
        self.session_middleware.process_request(self.request)
        self.request.session.save()
        cart = Cart(self.request)
        cart.add(self.product, quantity=2, override_quantity=False)
        response = cart_remove(self.request, self.product.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart:cart_detail'))
        self.assertEqual(len(cart), 0)

    def test_cart_detail(self):
        url = reverse('cart:cart_detail')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        self.assertIn('cart', response.context)
        self.assertIn('coupon_apply_form', response.context)

    def test_cart_add_invalid_form(self):
        url = reverse('cart:cart_add', args=[self.product.id])
        self.request = self.factory.post(url, data={'quantity': 0,
                                                    'override': False})
        self.request.user = self.user
        self.session_middleware.process_request(self.request)
        self.request.session.save()
        response = cart_add(self.request, self.product.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart:cart_detail'))

    def test_cart_remove_invalid_product(self):
        url = reverse('cart:cart_remove', args=[999])
        self.request = self.factory.post(url)
        self.request.user = self.user
        self.session_middleware.process_request(self.request)
        self.request.session.save()
        response = cart_remove(self.request, 999)
        self.assertEqual(response.status_code, 404)

    def test_cart_detail_with_coupon(self):
        url = reverse('cart:cart_detail')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        self.assertIn('coupon_apply_form', response.context)
        self.assertEqual(response.context['coupon_apply_form'].initial, {})

    def test_cart_add_override_quantity(self):
        url = reverse('cart:cart_add', args=[self.product.id])
        self.request = self.factory.post(url, data={'quantity': 2,
                                                    'override': True})
        self.request.user = self.user
        self.session_middleware.process_request(self.request)
        self.request.session.save()
        response = cart_add(self.request, self.product.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart:cart_detail'))
        cart = Cart(self.request)
        self.assertEqual(cart.cart[str(self.product.id)]['quantity'], 2)

    def test_cart_add_invalid_product(self):
        url = reverse('cart:cart_add', args=[999])
        self.request = self.factory.post(url, data={'quantity': 2,
                                                    'override': False})
        self.request.user = self.user
        self.session_middleware.process_request(self.request)
        self.request.session.save()
        response = cart_add(self.request, 999)
        self.assertEqual(response.status_code, 404)

    def test_cart_detail_empty_cart(self):
        url = reverse('cart:cart_detail')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        self.assertIn('cart', response.context)
        self.assertEqual(len(response.context['cart']), 0)
