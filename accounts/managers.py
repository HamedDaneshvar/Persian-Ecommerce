from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for the accounts app.

    This manager provides methods for creating and managing custom user models.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a new user.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.
            **extra_fields: Additional fields for the user model.

        Returns:
            User: The newly created user.

        Raises:
            ValueError: If the email is not provided.
        """

        if not email:
            raise ValueError(_('Users must have an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        """
        Creates and saves a new staff user.

        Args:
            email (str): The email address of the staff user.
            password (str): The password for the staff user.
            **extra_fields: Additional fields for the staff user model.

        Returns:
            User: The newly created staff user.

        Raises:
            ValueError: If is_staff is not set to True.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a new superuser.

        Args:
            email (str): The email address of the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields for the superuser model.

        Returns:
            User: The newly created superuser.

        Raises:
            ValueError: If is_staff or is_superuser is not set to True.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
