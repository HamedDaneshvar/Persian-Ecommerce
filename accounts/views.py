from django.shortcuts import (
    render,
    redirect,
)
from django.contrib.auth import (
    login,
    authenticate,
)
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from accounts.forms import (
    CustomUserCreationForm,
    ProfileForm,
)


def signup(request):
    """
    View function for user registration/signup.
    """

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            full_name = form.cleaned_data.get("full_name")
            raw_password = form.cleaned_data.get("password1")
            form = form.save(commit=False)
            form.username = email
            form.nick_name = full_name
            form.save()
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect("shop:product_list")
    else:
        form = CustomUserCreationForm()
    return render(request,
                  "accounts/signup.html",
                  {"form": form, })


@login_required
def profile(request):
    """
    View function to display user profile page.
    """

    return render(request,
                  "accounts/profile.html",)


@login_required
def edit_profile(request):
    """
<<<<<<< HEAD
    View function for editing user profile page.
=======
    View function for editing user profile.
>>>>>>> 2515f6f20d4c9e91ebb2f57c27dc5a36a88ea02f
    """

    user = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if "email" in form.changed_data:
                form.username = form.cleaned_data.get("email")
            form.save()
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=user)

    return render(request,
                  "accounts/edit_profile.html",
                  {"form": form, })
