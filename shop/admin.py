from django.contrib import admin
from .models import (
    Category,
    Product,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin class for managing Category model.
    """

    list_display = ["name", "slug"]
    # Automatically populate the slug field based on the name
    prepopulated_fields = {"slug": ("name",), }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin class for managing Product model.
    """

    list_display = ["name", "slug", "price", "available",
                    "create_at", "updated_at",]
    list_filter = ["available", "create_at", "updated_at",]
    # Editable fields directly in the admin list view
    list_editable = ["price", "available",]
    # Automatically populate the slug field based on the name
    prepopulated_fields = {"slug": ("name",), }
