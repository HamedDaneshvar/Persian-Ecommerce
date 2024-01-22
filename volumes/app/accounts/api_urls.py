from django.urls import path, include, re_path
from django.views.generic import TemplateView
from accounts.api import UserDetailAPIView

app_name = "accounts"

# API urls
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('user/', UserDetailAPIView.as_view(), name='rest_user_details'),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(
            template_name='dj_rest_auth/account_confirm_email.html'),
        name='account_confirm_email',
    ),
    path(
        'account-email-verification-sent/', TemplateView.as_view(
            template_name='dj_rest_auth/account_email_verification_sent.html'),
        name='account_email_verification_sent',
    ),
]
