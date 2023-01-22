from django.shortcuts import (
	render,
	redirect,
)
from django.contrib.auth import (
	login,
	authenticate,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from accounts.models import CustomUser
from .forms import (
	CustomUserCreationForm,
	ProfileForm,
)

def signup(request):
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
				  {"form": form,})

@login_required
def profile(request):
	return render(request,
				  "accounts/profile.html",)

@login_required
def edit_profile(request):
	user = CustomUser.objects.get(id=request.user.id)
	if request.method == "POST":
		profile_form = ProfileForm(request.POST, request.FILES, instance=user)
		profile_form.save()
		return redirect("accounts:profile")
	else:
		profile_form = ProfileForm(instance=user)

	return render(request,
				  "accounts/edit_profile.html",
				  {"profile_form": profile_form,})