from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin class for managing CustomUser model in the admin panel.
    """

    # Form used for creating a new custom user
    add_form = CustomUserCreationForm

    # Form used for updating an existing custom user
    form = CustomUserChangeForm

    model = CustomUser

    list_display = ["email", "username", "full_name", "phone",
                    "is_active", "is_staff", "is_superuser",
                    "last_login"]
    list_filter = ["is_active", "is_staff", "is_superuser",]

    # Defines the layout and grouping of fields displayed in the admin
    # panel for the CustomUser model
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'full_name',
                           'nick_name', 'phone', 'address', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )

    # Defines the layout and grouping of fields displayed in the admin
    # panel when adding a new custom user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'is_staff',
                       'is_active')}),
    )
    search_fields = ('email', 'username',)
    ordering = ('date_joined', 'email',)
