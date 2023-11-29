from django.db import models
from django.utils.translation import gettext as _


class GeneralModel(models.Model):
    """
    An abstract base model class that provides common fields for other models.

    Fields:
    - create_at: A DateTimeField representing the creation time of the
      model instance.
    - updated_at: A DateTimeField representing the last update time of
      the model instance.

    Meta:
    - abstract: Specifies that this model is an abstract base class and
      should not be used to create database tables.

    """
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created Time'),)
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated Time'),)

    class Meta:
        abstract = True
