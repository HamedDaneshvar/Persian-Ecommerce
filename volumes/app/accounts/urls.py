from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_view
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # default django url view
    path("login/", auth_view.LoginView.as_view(
            template_name="accounts/login.html"), name="login"),
    path("logout/", auth_view.LogoutView.as_view(), name="logout"),
    path(
        "password_change/", auth_view.PasswordChangeView.as_view(
            template_name="accounts/password_change_form.html"),
        name="password_change"),
    path(
        "password_change/done/",
        auth_view.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"),
        name="password_change_done",
    ),
    path(
        "password_reset/", auth_view.PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done")),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_view.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_view.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete")),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_view.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
