from django.contrib import admin
from orders.models import (
    Order,
    OrderItem
)


class OrderItemInline(admin.TabularInline):
    """
    Inline admin class for OrderItem model.

    This inline class allows the administration of OrderItem objects
    within the Order admin page in a tabular format.

    Attributes:
        - model (OrderItem): The model associated with the inline.
        - raw_id_fields (list): The fields displayed as raw ID fields in the
          admin interface.
    """
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin class for Order model.

    This class customizes the administration interface for the Order model.
    It defines the list display, list filters, and inline classes.

    Attributes:
        - list_display (list): The fields displayed in the list view of the
          admin interface.
        - list_filter (list): The fields used for filtering in the admin
          interface.
        - inlines (list): The inline classes associated with the Order admin
          page.
    """
    list_display = ["user", "full_name", "email", "phone", "address",
                    "transport", "get_total_cost", "paid",
                    "create_at", "updated_at"]
    list_filter = ["paid", "create_at", "updated_at",]
    inlines = [OrderItemInline]
