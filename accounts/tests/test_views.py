from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from accounts.models import CustomUser
from accounts.views import signup, profile, edit_profile


class AccountViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.signup_url = reverse('accounts:signup')
        self.profile_url = reverse('accounts:profile')
        self.edit_profile_url = reverse('accounts:edit_profile')

    def test_signup_view(self):
        form_data = {
            'email': 'test@example.com',
            'full_name': 'Test User',
            'password1': '2oireu8yr',
        }
        request = self.factory.post(self.signup_url, data=form_data)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = signup(request)
        # Check if it redirects after successful signup
        self.assertEqual(response.status_code, 302)

        # Check if the user is created and logged in
        user = CustomUser.objects.get(email='test@example.com')
        self.assertEqual(user.username, 'test@example.com')
        self.assertTrue(user.is_authenticated)

    def test_profile_view(self):
        user = CustomUser.objects.create_user(
            email='test@example.com', password='password'
        )
        request = self.factory.get(self.profile_url)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = user
        response = profile(request)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_view(self):
        user = CustomUser.objects.create_user(
            email='test@example.com', password='password'
        )
        request = self.factory.get(self.edit_profile_url)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = user
        response = edit_profile(request)
        self.assertEqual(response.status_code, 200)
        # Add more assertions specific to the edit_profile view

    def test_edit_profile_view_post(self):
        user = CustomUser.objects.create_user(
            email='test@example.com', password='password'
        )
        request = self.factory.post(self.edit_profile_url, data={
            'email': 'newemail@example.com',
            'full_name': 'New Name',
            # Add other fields to be updated
        })
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = user
        response = edit_profile(request)
        self.assertEqual(response.status_code, 302)
