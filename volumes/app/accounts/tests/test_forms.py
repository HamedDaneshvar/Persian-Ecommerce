from django.test import TestCase
from accounts.forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    ProfileForm,
)


class FormsTest(TestCase):
    def test_custom_user_creation_form(self):
        form_data = {
            'email': 'test@example.com',
            'full_name': 'John Doe',
            'password1': 'rj3o4ijr43o',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_with_password_too_common(self):
        form_data = {
            'email': 'test@example.com',
            'full_name': 'John Doe',
            'password1': 'Password'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_custom_user_change_form(self):
        form_data = {
            'email': 'test@example.com',
        }
        form = CustomUserChangeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_form(self):
        form_data = {
            'nick_name': 'JohnD',
            'full_name': 'John Doe',
            'phone': '1234567890',
            'email': 'test@example.com',
            'address': '123 Main St',
            'avatar': None,
        }
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_form_with_invalid_email(self):
        form_data = {
            'nick_name': 'JohnD',
            'full_name': 'John Doe',
            'phone': '1234567890',
            'email': '@example.com',
            'address': '123 Main St',
            'avatar': None,
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
