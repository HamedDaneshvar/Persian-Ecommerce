import os
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel
from .managers import CustomUserManager

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' %(uuid.uuid4(), ext)
    return os.path.join(f'users/', filename)


class CustomUser(AbstractUser, GeneralModel):
	first_name = None
	last_name = None
	full_name = models.CharField(max_length=128,
								 blank=True,
								 null=True,
								 verbose_name=_("Full name"),)
	nick_name = models.CharField(max_length=128,
								 blank=True,
								 null=True,
								 verbose_name=_("Nick name"),)
	email = models.EmailField(unique=True,
							  verbose_name=_("Email address"),)
	phone = models.CharField(max_length=13,
							 validators=[MinLengthValidator(10)],
							 blank=True,
							 null=True,
							 verbose_name=_("Phone"),)
	address = models.CharField(max_length=512,
							   blank=True,
							   null=True,
							   verbose_name=_("Address"),)
	avatar = models.ImageField(upload_to=get_file_path,
							   null=True,
							   blank=True,
							   verbose_name=_("Image profile"),)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	def __str__(self):
		return self.email