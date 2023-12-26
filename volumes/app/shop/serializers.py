from rest_framework import serializers
from shop.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    Fields:
        - url: Hyperlinked identity field for the category detail view.
        - name: Name of the category.
        - slug: Slug field for the category.

    Excluded Fields:
        - create_at: Excluded from serialization.
        - updated_at: Excluded from serialization.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='api-shop:category-detail',
    )

    class Meta:
        model = Category
        exclude = ['create_at', 'updated_at',]


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    Fields:
        - url: Hyperlinked identity field for the product detail view.
        - category: Nested serializer for the associated category.
        - name: Name of the product.
        - price: Price of the product.
        - slug: Slug field for the product.
        - image: Image field for the product.
        - description: Description of the product.

    Excluded Fields:
        - create_at: Excluded from serialization.
        - updated_at: Excluded from serialization.
        - available: Excluded from serialization if the requesting user is not
        a staff member.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='api-shop:product-detail',
    )
    category = CategorySerializer()

    class Meta:
        model = Product
        exclude = ['create_at', 'updated_at',]

    def get_fields(self):
        fields = super().get_fields()
        if not self.context['request'].user.is_staff:
            fields.pop('available', None)
        return fields
