from django.contrib import admin
from reviews.models import Review

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "get_full_name", "rate", "create_at", "status"]
    list_filter = ["status", "create_at"]
