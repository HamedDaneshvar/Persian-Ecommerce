from django.db import models
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel


class Transport(GeneralModel):
    """
    Represents a transport option for delivery in the e-commerce system.

    Attributes:
        - name (str): The name of the transport option.
        - delivery (str): The description of the delivery service.
        - price (Decimal): The price of the transport option.
        - activate (bool): Indicates whether the transport option is currently
          active.

    Methods:
        - __str__: Returns a string representation of the transport option.

    """
    name = models.CharField(max_length=255,
                            verbose_name=_("Name"),)
    delivery = models.CharField(max_length=225,
                                verbose_name=_("Delivery"),)
    price = models.DecimalField(max_digits=12,
                                decimal_places=2,
                                verbose_name=_("Price"),)
    activate = models.BooleanField(verbose_name=_("Activate"))

    def __str__(self):
        return f"{self.name}: {self.delivery}"
