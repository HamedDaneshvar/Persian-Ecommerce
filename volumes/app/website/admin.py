from django.contrib import admin
from website.models import Slider


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'status']
    list_editable = ['subtitle', 'status']
    list_filter = ['status', 'create_at', 'updated_at',]
