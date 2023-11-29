from django.contrib import admin
from transportation.models import Transport


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Transport model.

    This class defines the administration interface for the Transport model in
    the Django admin site. It specifies the list of fields to be displayed in
    the list view, and allows editing of the price and activation fields
    directly in the list view.

    Attributes:
        - list_display (list): The fields to be displayed in the list view of
          the admin site.
        - list_editable (list): The fields that can be edited directly in the
          list view of the admin site.

    """
    list_display = ["name", "delivery", "price", "activate"]
    list_editable = ["price", "activate"]
