from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from utils.general_model import GeneralModel


class Coupon(GeneralModel):
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
