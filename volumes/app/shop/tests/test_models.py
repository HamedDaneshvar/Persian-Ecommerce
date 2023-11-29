from django.test import TestCase
from django.urls import reverse
from shop.models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )

    def test_category_name(self):
        self.assertEqual(str(self.category), 'Electronics')

    def test_category_absolute_url(self):
        url = reverse('shop:product_list_by_category',
                      args=[self.category.slug])
        self.assertEqual(self.category.get_absolute_url(), url)


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Laptop',
            slug='laptop',
            price=999.99,
            available=True
        )

    def test_product_name(self):
        self.assertEqual(str(self.product), 'Laptop')

    def test_product_absolute_url(self):
        url = reverse('shop:product_detail',
                      args=[self.product.id, self.product.slug])
        self.assertEqual(self.product.get_absolute_url(), url)


class ModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Clothing',
            slug='clothing'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Shirt',
            slug='shirt',
            price=19.99,
            available=True
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Clothing')
        self.assertEqual(self.category.slug, 'clothing')
        self.assertEqual(str(self.category), 'Clothing')
        self.assertEqual(self.category.get_absolute_url(),
                         reverse('shop:product_list_by_category',
                                 args=['clothing']))

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Shirt')
        self.assertEqual(self.product.slug, 'shirt')
        self.assertEqual(self.product.price, 19.99)
        self.assertEqual(self.product.available, True)
        self.assertEqual(str(self.product), 'Shirt')
        self.assertEqual(self.product.get_absolute_url(),
                         reverse('shop:product_detail',
                                 args=[self.product.id, 'shirt']))
