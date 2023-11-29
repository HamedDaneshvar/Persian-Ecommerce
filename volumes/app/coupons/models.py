from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.core.exceptions import ValidationError
from utils.general_model import GeneralModel


class Coupon(GeneralModel):
    """
    Represents a coupon that can be applied to a purchase in the e-commerce
    system.

    Attributes:
    - code (str): The unique code for the coupon.
    - valid_from (datetime): The date and time from which the coupon is valid.
    - valid_to (datetime): The date and time until which the coupon is valid.
    - discount (int): The percentage value of the discount (0 to 100).
    - active (bool): Indicates whether the coupon is currently active.

    Methods:
    - __str__: Returns a string representation of the coupon (the code).

    """
    code = models.CharField(max_length=50,
                            unique=True,
                            verbose_name=_("Code"),)
    valid_from = models.DateTimeField(verbose_name=_("Valid from"))
    valid_to = models.DateTimeField(verbose_name=_("Valid to"))
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("Percentage value (0 to 100)"))
    active = models.BooleanField(verbose_name=_("Active"))

    def __str__(self):
        return self.code

    def clean(self):
        if self.discount < 0 or self.discount > 100:
            raise ValidationError("Discount must be between 0 and 100.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def is_valid(self):
        """
        Checks if the coupon is currently valid based on the valid_from and
        valid_to attributes.

        Returns:
            bool: True if the coupon is valid, False otherwise.
        """
        now = timezone.now()
        return self.valid_from <= now <= self.valid_to
