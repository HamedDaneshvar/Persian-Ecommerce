from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel

validate_merchant = RegexValidator(
    regex=r'.{8}\-.{4}\-.{4}\-.{4}\-.{12}',
    message="Merchant must be exactly 36 characters and like Zarinpal" +
            "merchant be",
    code="invalid_length"
)


class Payment(GeneralModel):
    payment_choices = (
        ("zarinpal", _("Zarinpal Payment Gateway")),
    )
    name = models.CharField(max_length=250,
                            verbose_name=_("Name"))
    merchant = models.CharField(max_length=36,
                                validators=[validate_merchant,],
                                verbose_name=_("Merchant"))
    types = models.CharField(max_length=50,
                             choices=payment_choices,
                             unique=True,
                             verbose_name=_("Payment Type"))
    available = models.BooleanField(default=True,
                                    verbose_name=_("Available"),)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def save(self, *args, **kwargs):
        try:
            validate_merchant(self.merchant)
        except ValidationError as e:
            raise ValueError(e.message)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.get_types_display()}"
