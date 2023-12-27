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
        - category_id: Primary key related field for selecting an existing
        category.

    Excluded Fields:
        - create_at: Excluded from serialization.
        - updated_at: Excluded from serialization.
        - available: Excluded from serialization if the requesting user is not
        a staff member.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='api-shop:product-detail',
    )
    # Show category information when retrieving product list
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        # Allow selecting from existing categories
        queryset=Category.objects.all(),
        write_only=True,  # Exclude category field when retrieving product list
        required=True  # Require category field for POST requests
    )

    class Meta:
        model = Product
        exclude = ['create_at', 'updated_at',]

    def get_fields(self):
        fields = super().get_fields()
        if not self.context['request'].user.is_staff:
            fields.pop('available', None)
        return fields

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        validated_data['category'] = category_id
        return super().create(validated_data)
