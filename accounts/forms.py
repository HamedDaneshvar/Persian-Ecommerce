from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
	UserCreationForm,
	UserChangeForm,
)
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	password2 = None
	
	class Meta:
		model = CustomUser
		fields = ("email", "full_name")

	def _post_clean(self):
		super()._post_clean()
		# Validate the password after self.instance is updated with form data
		# by super().
		password = self.cleaned_data.get('password1')
		if password:
			try:
				password_validation.validate_password(password, self.instance)
			except ValidationError as error:
				self.add_error('password1', error)


class CustomUserChangeForm(UserChangeForm):
	
	class Meta:
		model = CustomUser
		fields = ("email",)


class ProfileForm(forms.ModelForm):
	# initial_data = {
	# 	"nick_name": ,
	# 	"full_name": ,
	# 	"phone": ,
	# 	"email": ,
	# 	"address": ,
	# 	"avatar": ,
	# }
	
	class Meta:
		model = CustomUser
		fields = ("nick_name", "full_name", "phone",
				  "email", "address", "avatar",)
		