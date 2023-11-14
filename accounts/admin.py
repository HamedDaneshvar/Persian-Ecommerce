from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser

    list_display = ["email", "username", "full_name", "phone",
                    "is_active", "is_staff", "is_superuser",
                    "last_login"]
    list_filter = ["is_active", "is_staff", "is_superuser",]
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'full_name',
                           'nick_name', 'phone', 'address', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'is_staff',
                       'is_active')}),
    )
    search_fields = ('email', 'username',)
    ordering = ('date_joined', 'email',)
