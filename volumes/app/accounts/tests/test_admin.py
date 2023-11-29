from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from accounts.admin import CustomUserAdmin
from accounts.models import CustomUser


class CustomUserAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = CustomUserAdmin(CustomUser, self.site)

    def test_list_display(self):
        self.assertEqual(
            self.admin.list_display,
            ["email", "username", "full_name", "phone", "is_active",
             "is_staff", "is_superuser", "last_login"]
        )

    def test_list_filter(self):
        self.assertEqual(
            self.admin.list_filter,
            ["is_active", "is_staff", "is_superuser"]
        )

    def test_fieldsets(self):
        fieldsets = self.admin.fieldsets
        self.assertEqual(len(fieldsets), 3)
        self.assertEqual(fieldsets[0][0], None)
        self.assertEqual(fieldsets[1][0], 'Permissions')
        self.assertEqual(fieldsets[2][0], 'Dates')

    def test_add_fieldsets(self):
        add_fieldsets = self.admin.add_fieldsets
        self.assertEqual(len(add_fieldsets), 1)
        self.assertEqual(add_fieldsets[0][0], None)
        self.assertEqual(add_fieldsets[0][1]['classes'], ('wide',))

    def test_search_fields(self):
        self.assertEqual(
            self.admin.search_fields,
            ('email', 'username')
        )

    def test_ordering(self):
        self.assertEqual(
            self.admin.ordering,
            ('date_joined', 'email')
        )
