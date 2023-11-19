from django.contrib import admin
from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["name", "types", "available",
                    "create_at", "updated_at",]
    list_filter = ["available", "create_at", "updated_at",]
