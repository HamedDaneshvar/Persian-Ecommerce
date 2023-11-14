import os
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel
from .managers import CustomUserManager


def get_file_path(instance, filename):
    """
    Function to generate a unique file path for user avatar.

    Args:
        instance: The instance of the user model.
        filename (str): The original filename of the uploaded file.

    Returns:
        str: The unique file path for the user avatar.
    """

    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join('users/', filename)


class CustomUser(AbstractUser, GeneralModel):
    """
    Custom user model for the accounts app.

    This model extends the AbstractUser class provided by Django and adds
    additional fields.
    """

    first_name = None
    last_name = None
    full_name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_("Full name"),
    )
    nick_name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_("Nick name"),
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email address"),
    )
    phone = models.CharField(
        max_length=13,
        validators=[MinLengthValidator(10)],
        blank=True,
        null=True,
        verbose_name=_("Phone"),
    )
    address = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        verbose_name=_("Address"),
    )
    avatar = models.ImageField(
        upload_to=get_file_path,
        null=True,
        blank=True,
        verbose_name=_("Image profile"),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        """
        Override the save method to set the username as the email address.

        This method automatically sets the value of the username field as
        the value of the email field when a CustomUser instance is saved.

        Args:
            *args: Additional positional arguments passed to the save method.
            **kwargs: Additional keyword arguments passed to the save method.
        """
        self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Get a string representation of the user.

        Returns:
            str: The email address of the user.
        """

        return self.email
