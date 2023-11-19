from django.contrib import admin
from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Payment model.

    Attributes:
        - list_display (list): The list of fields to display in the admin list
          view.
        - list_filter (list): The list of fields to use for filtering in the
          admin list view.
    """
    list_display = ["name", "types", "available",
                    "create_at", "updated_at",]
    list_filter = ["available", "create_at", "updated_at",]
