from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new custom user.

    This form extends the UserCreationForm provided by Django and adds
    additional validation for the password field.

    Attributes:
        password2: Field to confirm the password and set to None to remove
    """

    password2 = None

    class Meta:
        model = CustomUser
        fields = ("email", "full_name")

    def _post_clean(self):
        """
        Perform additional validation after the form is cleaned.

        This method validates the password field using the password_validation
        module.
        If any validation error occurs, it adds the error to the 'password1'
        field.
        """

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
    """
    Form for updating an existing custom user.

    This form extends the UserChangeForm provided by Django.

    Attributes:
        model: The custom user model to be used.
        fields: The fields to be displayed in the form.
    """

    class Meta:
        model = CustomUser
        fields = ("email",)


class ProfileForm(forms.ModelForm):
    """
    Form for updating the user profile.

    This form is used to update fields such as nick_name, full_name, phone,
    email, address, and avatar.

    Attributes:
        model: The custom user model to be used.
        fields: The fields to be displayed in the form.
    """

    class Meta:
        model = CustomUser
        fields = ("nick_name", "full_name", "phone",
                  "email", "address", "avatar",)
