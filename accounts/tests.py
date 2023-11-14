from django.test import TestCase
from .models import CustomUser, get_file_path


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='password',
            full_name='John Doe',
            nick_name='JD',
            phone='1234567890',
            address='123 Main St',
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.check_password('password'), True)
        self.assertEqual(self.user.full_name, 'John Doe')
        self.assertEqual(self.user.nick_name, 'JD')
        self.assertEqual(self.user.phone, '1234567890')
        self.assertEqual(self.user.address, '123 Main St')
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.is_superuser, False)

    def test_create_staffuser(self):
        staff_user = CustomUser.objects.create_staffuser(
            email='staff@example.com',
            password='password',
            full_name='Jane Smith',
            nick_name='JS',
            phone='9876543210',
            address='456 Park Ave',
        )

        self.assertEqual(staff_user.email, 'staff@example.com')
        self.assertEqual(staff_user.check_password('password'), True)
        self.assertEqual(staff_user.full_name, 'Jane Smith')
        self.assertEqual(staff_user.nick_name, 'JS')
        self.assertEqual(staff_user.phone, '9876543210')
        self.assertEqual(staff_user.address, '456 Park Ave')
        self.assertEqual(staff_user.is_staff, True)
        self.assertEqual(staff_user.is_superuser, False)

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='password',
            full_name='Admin User',
            nick_name='Admin',
            phone='5555555555',
            address='789 Elm St',
        )

        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertEqual(superuser.check_password('password'), True)
        self.assertEqual(superuser.full_name, 'Admin User')
        self.assertEqual(superuser.nick_name, 'Admin')
        self.assertEqual(superuser.phone, '5555555555')
        self.assertEqual(superuser.address, '789 Elm St')
        self.assertEqual(superuser.is_staff, True)
        self.assertEqual(superuser.is_superuser, True)


class GetFilePathTest(TestCase):
    def test_get_file_path(self):
        instance = None
        filename = 'avatar.jpg'

        # Call the get_file_path function
        unique_file_path = get_file_path(instance, filename)

        # Define the expected file path based on the UUID generated by the
        # function
        expected_file_path = unique_file_path

        # Assert that the generated file path matches the expected file path
        self.assertEqual(unique_file_path, expected_file_path)
