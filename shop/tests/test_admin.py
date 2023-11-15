from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from shop.admin import CategoryAdmin, ProductAdmin
from shop.models import Category, Product


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_staff(self):
        return True


class AdminTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()

    def test_category_admin(self):
        model_admin = CategoryAdmin(Category, self.site)
        self.assertEqual(model_admin.list_display, ["name", "slug"])
        self.assertEqual(list(model_admin.prepopulated_fields.keys()),
                         ["slug"])
        self.assertEqual(list(model_admin.prepopulated_fields.values()),
                         [("name",)])

    def test_product_admin(self):
        model_admin = ProductAdmin(Product, self.site)
        self.assertEqual(
            model_admin.list_display,
            ["name", "slug", "price", "available", "create_at", "updated_at"],
        )
        self.assertEqual(
            model_admin.list_filter,
            ["available", "create_at", "updated_at"],
        )
        self.assertEqual(
            model_admin.list_editable,
            ["price", "available"],
        )
        self.assertEqual(list(model_admin.prepopulated_fields.keys()),
                         ["slug"])
        self.assertEqual(list(model_admin.prepopulated_fields.values()),
                         [("name",)])

    def test_category_admin_changelist_view(self):
        request = self.factory.get('/admin/shop/category/')
        request.user = MockSuperUser()
        model_admin = CategoryAdmin(Category, self.site)
        response = model_admin.changelist_view(request)
        self.assertEqual(response.status_code, 200)

    def test_product_admin_changelist_view(self):
        request = self.factory.get('/admin/shop/product/')
        request.user = MockSuperUser()
        model_admin = ProductAdmin(Product, self.site)
        response = model_admin.changelist_view(request)
        self.assertEqual(response.status_code, 200)

    def test_category_admin_change_view(self):
        category = Category.objects.create(name='Electronics',
                                           slug='electronics')
        request = self.factory.get(
            f'/admin/shop/category/{category.id}/change/')
        request.user = MockSuperUser()
        model_admin = CategoryAdmin(Category, self.site)
        response = model_admin.change_view(request, str(category.id))
        self.assertEqual(response.status_code, 200)

    def test_product_admin_change_view(self):
        category = Category.objects.create(name='Electronics',
                                           slug='electronics')
        product = Product.objects.create(category=category, name='Laptop',
                                         slug='laptop', price=999.99,
                                         available=True)
        request = self.factory.get(f'/admin/shop/product/{product.id}/change/')
        request.user = MockSuperUser()
        model_admin = ProductAdmin(Product, self.site)
        response = model_admin.change_view(request, str(product.id))
        self.assertEqual(response.status_code, 200)

    def test_category_admin_add_view(self):
        request = self.factory.get('/admin/shop/category/add/')
        request.user = MockSuperUser()
        model_admin = CategoryAdmin(Category, self.site)
        response = model_admin.add_view(request)
        self.assertEqual(response.status_code, 200)

    def test_product_admin_add_view(self):
        request = self.factory.get('/admin/shop/product/add/')
        request.user = MockSuperUser()
        model_admin = ProductAdmin(Product, self.site)
        response = model_admin.add_view(request)
        self.assertEqual(response.status_code, 200)
