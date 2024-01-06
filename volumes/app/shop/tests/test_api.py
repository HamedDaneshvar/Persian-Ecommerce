from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from shop.models import Category, Product
from shop.serializers import CategorySerializer, ProductSerializer


User = get_user_model()


class CategoryAPITestCase(APITestCase):
    def setUp(self):
        self.user = self.create_superuser()
<<<<<<< HEAD
        self.category = Category.objects.create(name='Test Category',
                                                slug='test-category')
        self.url = reverse('api-shop:category-detail',
                           kwargs={'pk': self.category.pk})
        factory = RequestFactory()
        request = factory.get(self.url)
        self.serializer_data = CategorySerializer(
            self.category, context={'request': request}).data
=======
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.url = reverse('api-shop:category-detail', kwargs={'pk': self.category.pk})
        factory = RequestFactory()
        request = factory.get(self.url)
        self.serializer_data = CategorySerializer(self.category, context={'request': request}).data
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab

    def create_superuser(self):
        user = User.objects.create_superuser(
            email='test@example.com',
            password='testpass',
            full_name='John Doe'
        )
        return user

    def test_retrieve_category(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.serializer_data)

    def test_update_category(self):
        new_data = {'name': 'Updated Category', 'slug': 'updated-category'}
        self.client.force_login(self.user)
        response = self.client.put(self.url, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])
        self.assertEqual(response.data['slug'], new_data['slug'])

    def test_delete_category(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())

    def test_create_category_unauthorized(self):
        data = {'name': 'New Category', 'slug': 'new-category'}
<<<<<<< HEAD
        response = self.client.post(reverse('api-shop:category-list-create'),
                                    data)
=======
        response = self.client.post(reverse('api-shop:category-list-create'), data)
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Category.objects.filter(name='New Category').exists())

    def test_create_category_authorized(self):
<<<<<<< HEAD
        user = User.objects.create_superuser(username='admin@example.com',
                                             email='admin@example.com',
                                             password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': 'New Category', 'slug': 'new-category'}
        response = self.client.post(reverse('api-shop:category-list-create'),
                                    data)
=======
        user = User.objects.create_superuser(username='admin@example.com', email='admin@example.com',  password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': 'New Category', 'slug': 'new-category'}
        response = self.client.post(reverse('api-shop:category-list-create'), data)
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name='New Category').exists())


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.user = self.create_superuser()
<<<<<<< HEAD
        self.category = Category.objects.create(name='Test Category',
                                                slug='test-category')
        self.product = Product.objects.create(name='Test Product',
                                              slug='test-product',
                                              price=10.99,
                                              category=self.category)
        self.url = reverse('api-shop:product-detail',
                           kwargs={'pk': self.product.pk})
        factory = RequestFactory()
        request = factory.get(self.url)
        self.serializer_data = ProductSerializer(
            self.product, context={'request': request}).data
=======
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(name='Test Product', slug='test-product', price=10.99, category=self.category)
        self.url = reverse('api-shop:product-detail', kwargs={'pk': self.product.pk})
        factory = RequestFactory()
        request = factory.get(self.url)
        self.serializer_data = ProductSerializer(self.product, context={'request': request}).data
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab

    def create_superuser(self):
        user = User.objects.create_superuser(
            email='test@example.com',
            password='testpass',
            full_name='John Doe'
        )
        return user

    def test_retrieve_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.serializer_data)

    def test_update_product(self):
        self.client.force_login(self.user)
<<<<<<< HEAD
        new_data = {'name': 'Updated Product',
                    'slug': 'updated-product',
                    'price': '19.99',
                    'category_id': self.category.pk}
=======
        new_data = {'name': 'Updated Product', 'slug':'updated-product', 'price': '19.99', 'category_id': self.category.pk}
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab
        response = self.client.put(self.url, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])
        self.assertEqual(response.data['slug'], new_data['slug'])
        self.assertEqual(response.data['price'], new_data['price'])

    def test_delete_product(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_create_product_unauthorized(self):
<<<<<<< HEAD
        data = {'name': 'New Product', 'price': 9.99,
                'category_id': self.category.pk}
        response = self.client.post(reverse('api-shop:product-list-create'),
                                    data)
=======
        data = {'name': 'New Product', 'price': 9.99, 'category_id': self.category.pk}
        response = self.client.post(reverse('api-shop:product-list-create'), data)
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Product.objects.filter(name='New Product').exists())

    def test_create_product_authorized(self):
<<<<<<< HEAD
        user = User.objects.create_superuser(username='admin@example.com',
                                             email='admin@example.com',
                                             password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': 'New Product', 'slug': 'new-product', 'price': 9.99,
                'category_id': self.category.pk}
        response = self.client.post(reverse('api-shop:product-list-create'),
                                    data)
=======
        user = User.objects.create_superuser(username='admin@example.com', email='admin@example.com',  password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': 'New Product', 'slug': 'new-product', 'price': 9.99, 'category_id': self.category.pk}
        response = self.client.post(reverse('api-shop:product-list-create'), data)
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name='New Product').exists())


class ProductListAPITestCase(APITestCase):
    def setUp(self):
<<<<<<< HEAD
        self.category = Category.objects.create(name='Test Category',
                                                slug='test-category')
        Product.objects.create(name='Product 1', slug='product-1',
                               price=10.99, category=self.category,
                               available=True)
        Product.objects.create(name='Product 2', slug='product-2',
                               price=19.99, category=self.category,
                               available=False)
=======
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        Product.objects.create(name='Product 1', slug='product-1', price=10.99, category=self.category, available=True)
        Product.objects.create(name='Product 2', slug='product-2', price=19.99, category=self.category, available=False)
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab

    def test_list_products_unauthorized(self):
        response = self.client.get(reverse('api-shop:product-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
<<<<<<< HEAD
        # Only one available product should be returned.
        self.assertEqual(len(response.data), 1)

    def test_list_products_authorized(self):
        user = User.objects.create_superuser(username='admin@example.com',
                                             email='admin@example.com',
                                             password='admin123')
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('api-shop:product-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Both products should be returned.
        self.assertEqual(len(response.data), 2)

    def test_create_product_unauthorized(self):
        data = {'name': 'New Product', 'price': 9.99,
                'category_id': self.category.pk}
        response = self.client.post(reverse('api-shop:product-list-create'),
                                    data)
=======
        self.assertEqual(len(response.data), 1)  # Only one available product should be returned.

    def test_list_products_authorized(self):
        user = User.objects.create_superuser(username='admin@example.com', email='admin@example.com',  password='admin123')
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('api-shop:product-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both products should be returned.

    def test_create_product_unauthorized(self):
        data = {'name': 'New Product', 'price': 9.99, 'category_id': self.category.pk}
        response = self.client.post(reverse('api-shop:product-list-create'), data)
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Product.objects.filter(name='New Product').exists())

    def test_create_product_authorized(self):
<<<<<<< HEAD
        user = User.objects.create_superuser(username='admin@example.com',
                                             email='admin@example.com',
                                             password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': 'New Product', 'slug': 'new-product', 'price': 9.99,
                'category_id': self.category.pk}
        response = self.client.post(reverse('api-shop:product-list-create'),
                                    data)
=======
        user = User.objects.create_superuser(username='admin@example.com', email='admin@example.com',  password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': 'New Product', 'slug': 'new-product', 'price': 9.99, 'category_id': self.category.pk}
        response = self.client.post(reverse('api-shop:product-list-create'), data)
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name='New Product').exists())

    def test_create_product_missing_category(self):
<<<<<<< HEAD
        user = User.objects.create_superuser(username='admin@example.com',
                                             email='admin@example.com',
                                             password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': 'New Product', 'price': 9.99}
        response = self.client.post(reverse('api-shop:product-list-create'),
                                    data)
=======
        user = User.objects.create_superuser(username='admin@example.com', email='admin@example.com',  password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': 'New Product', 'price': 9.99}
        response = self.client.post(reverse('api-shop:product-list-create'), data)
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Product.objects.filter(name='New Product').exists())

    def test_create_product_invalid_category(self):
<<<<<<< HEAD
        user = User.objects.create_superuser(username='admin@example.com',
                                             email='admin@example.com',
                                             password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': 'New Product', 'slug': 'new-product', 'price': 9.99,
                'category_id': 999}  # Non-existent category ID
        response = self.client.post(reverse('api-shop:product-list-create'),
                                    data)
=======
        user = User.objects.create_superuser(username='admin@example.com', email='admin@example.com',  password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': 'New Product', 'slug': 'new-product', 'price': 9.99, 'category_id': 999}  # Non-existent category ID
        response = self.client.post(reverse('api-shop:product-list-create'), data)
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Product.objects.filter(name='New Product').exists())

    def test_create_product_invalid_price(self):
<<<<<<< HEAD
        user = User.objects.create_superuser(username='admin@example.com',
                                             email='admin@example.com',
                                             password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': 'New Product', 'slug': 'new-product',
                'price': 'invalid', 'category_id': self.category.pk}
        response = self.client.post(reverse('api-shop:product-list-create'),
                                    data)
=======
        user = User.objects.create_superuser(username='admin@example.com', email='admin@example.com',  password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': 'New Product', 'slug': 'new-product', 'price': 'invalid', 'category_id': self.category.pk}
        response = self.client.post(reverse('api-shop:product-list-create'), data)
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Product.objects.filter(name='New Product').exists())

    def test_create_product_invalid_name(self):
<<<<<<< HEAD
        user = User.objects.create_superuser(username='admin@example.com',
                                             email='admin@example.com',
                                             password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': '', 'slug': 'new-product', 'price': 9.99,
                'category_id': self.category.pk}
        response = self.client.post(reverse('api-shop:product-list-create'),
                                    data)
=======
        user = User.objects.create_superuser(username='admin@example.com', email='admin@example.com',  password='admin123')
        self.client.force_authenticate(user=user)
        data = {'name': '', 'slug': 'new-product', 'price': 9.99, 'category_id': self.category.pk}
        response = self.client.post(reverse('api-shop:product-list-create'), data)
>>>>>>> 6f148bd5c28ac6b554188f29e5165117dc5df2ab
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Product.objects.filter(name='').exists())
