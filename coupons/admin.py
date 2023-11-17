from django.contrib import admin
from coupons.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Coupon model.

    This class defines the admin interface for managing Coupon objects in the
    Django admin site. It provides customization options for how Coupon
    objects are displayed and filtered in the admin interface.

    Attributes:
        list_display (list): The fields to display for each Coupon object in
                             the list view of the admin interface.
        list_filter (list): The fields to use for filtering the Coupon objects
                            in the admin interface.
        search_fields (list): The fields to use for searching Coupon objects
                              in the admin interface.

    Example:
        To access the Coupon admin interface, go to the Django admin site and
        navigate to the Coupons section. Here, you can view, add, edit, and
        delete Coupon objects, and the admin interface will display the
        specified fields.

    """
    list_display = ["code", "valid_from", "valid_to",
                    "discount", "active",]
    list_filter = ["active", "valid_from", "valid_to",]
    search_fields = ["code",]
