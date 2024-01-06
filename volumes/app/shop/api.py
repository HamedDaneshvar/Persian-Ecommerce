from rest_framework import generics, permissions
from shop.serializers import ProductSerializer, CategorySerializer
from shop.models import Product, Category


class CategoryListCreateAPI(generics.ListCreateAPIView):
    """
    API view for listing and creating categories.

    Permissions:
        - GET: Allow any user to retrieve the list of categories.
        - POST: Only admin users are allowed to create new categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]


class CategoryDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a category.

    Permissions:
        - GET: Allow any user to retrieve a category.
        - PUT/PATCH/DELETE: Only admin users are allowed to update or delete a
        category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]


class ProductListCreateAPI(generics.ListCreateAPIView):
    """
    API view for listing and creating products.

    Permissions:
        - GET: Allow any user to retrieve the list of products.
        - POST: Only admin users are allowed to create new products.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Product.objects.all()
        else:
            return Product.objects.filter(available=True)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]


class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a product.

    Permissions:
        - GET: Allow any user to retrieve a product.
        - PUT/PATCH/DELETE: Only admin users are allowed to update or delete a
        product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]
