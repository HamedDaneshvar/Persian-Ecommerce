from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Category, Product
from cart.forms import CartAddProductForm


class ProductListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category',
                                                slug='test-category')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            slug='test_product',
            price=9.99,
            available=True
        )
        self.url = reverse('shop:product_list')

    def test_product_list_without_category_slug(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['category'], None)

    def test_product_list_with_category_slug(self):
        url = reverse('shop:product_list_by_category',
                      args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['category'], self.category)

    def test_product_list_no_products_exist(self):
        Product.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertEqual(len(response.context['products']), 0)
        self.assertFalse(response.context['product_exist'])
        self.assertEqual(
            response.context['products_description'],
            "این فروشگاه محصولی را ثبت نکرده است."
        )

    def test_product_list_no_products_exist_for_category(self):
        Product.objects.all().delete()
        url = reverse('shop:product_list_by_category',
                      args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertEqual(len(response.context['products']), 0)
        self.assertFalse(response.context['product_exist'])
        self.assertEqual(
            response.context['products_description'],
            # "برای این دسته‌بندی محصولی ثبت نشده است."
            "این فروشگاه محصولی را ثبت نکرده است."
        )

    def test_product_list_grid_view(self):
        response = self.client.get(self.url, {'style': 'grid'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertTrue(response.context['grid'])

    def test_product_list_list_view(self):
        response = self.client.get(self.url, {'style': 'list'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertFalse(response.context['grid'])

    def test_product_list_cart_product_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertIsInstance(
            response.context['cart_product_form'],
            CartAddProductForm
        )


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category',
                                                slug='test-category')

        # Create a temporary image file for testing
        from django.core.files.uploadedfile import SimpleUploadedFile
        image = SimpleUploadedFile(name='test_image.jpg', content=b'',
                                   content_type='image/jpeg')

        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            slug='test_product',
            price=9.99,
            image=image,
            available=True
        )
        self.url = reverse('shop:product_detail',
                           args=[self.product.id, self.product.slug])

    def test_product_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/detail.html')
        self.assertEqual(response.context['product'], self.product)

    def test_product_detail_view_unavailable_product(self):
        self.product.available = False
        self.product.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_product_detail_view_invalid_product_id(self):
        url = reverse('shop:product_detail', args=[999, self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_product_detail_view_invalid_product_slug(self):
        url = reverse('shop:product_detail',
                      args=[self.product.id, 'invalid-slug'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_product_detail_view_cart_product_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/detail.html')
        self.assertIsInstance(
            response.context['cart_product_form'],
            CartAddProductForm
        )
