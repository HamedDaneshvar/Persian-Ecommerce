from decimal import Decimal
from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel
from shop.models import Product
from coupons.models import Coupon
from transportation.models import Transport


class Order(GeneralModel):
    """
    Model representing an order.

    This model stores information about an order placed by a customer.
    It includes details such as the associated coupon, transport, customer
    information, order status, and total cost.

    Attributes:
        - coupon (ForeignKey): The associated coupon for the order.
        - transport (ForeignKey): The transport method chosen for the order.
        - full_name (CharField): The full name of the customer.
        - email (EmailField): The email address of the customer.
        - phone (CharField): The phone number of the customer.
        - address (CharField): The address for the delivery.
        - paid (BooleanField): Indicates if the order has been paid.
        - discount (IntegerField): The discount percentage for the order.
        - transaction_id (IntegerField): The transaction ID for the order
          payment.
        - fee (DecimalField): The additional fee for the order.
    """
    coupon = models.ForeignKey(Coupon,
                               on_delete=models.SET_NULL,
                               related_name="orders",
                               null=True,
                               blank=True,)
    transport = models.ForeignKey(Transport,
                                  on_delete=models.SET_NULL,
                                  related_name="orders_transport",
                                  null=True,)
    full_name = models.CharField(max_length=128,
                                 verbose_name=_("Full name"))
    email = models.EmailField(verbose_name=_("E-mail"))
    phone = models.CharField(max_length=11,
                             verbose_name=_("Phone"),)
    address = models.CharField(max_length=512,
                               verbose_name=_("Address"))
    paid = models.BooleanField(default=False,
                               verbose_name=_("Paid"))
    discount = models.IntegerField(default=0,
                                   validators=[
                                       MinValueValidator(0),
                                       MaxValueValidator(100),])
    transaction_id = models.IntegerField(verbose_name=_("Transaction ID"),
                                         null=True)
    fee = models.DecimalField(max_digits=10,
                              decimal_places=2,
                              default=0,
                              verbose_name=_("Fee"))

    class Meta:
        ordering = ["-create_at"]
        indexes = [
            models.Index(fields=["-create_at"]),
        ]

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost_before_discount(self):
        """
        Calculate the total cost of the order items before applying any
        discount.

        Returns:
            Decimal: The total cost before discount.
        """
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        """
        Calculate the discount amount for the order.

        Returns:
            Decimal: The discount amount.
        """
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        """
        Calculate the total cost of the order, including any additional fees
        and discounts.

        Returns:
            str: The total cost of the order as a string.
        """
        transport_price = Decimal(0)
        if self.transport:
            transport_price = self.transport.price
        total_cost = self.get_total_cost_before_discount() + transport_price
        return str(total_cost - self.get_discount())
    get_total_cost.short_description = _("Total cost")


class OrderItem(GeneralModel):
    """
    Model representing an item within an order.

    This model stores information about an item included in an order.
    It includes details such as the associated order, product, price, and
    quantity.

    Attributes:
        - order (ForeignKey): The associated order for the item.
        - product (ForeignKey): The associated product for the item.
        - price (DecimalField): The price of the item.
        - quantity (PositiveIntegerField): The quantity of the item.
    """
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name="items",)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="order_items",)
    price = models.DecimalField(max_digits=12,
                                decimal_places=2,
                                verbose_name=_("Price"))
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name=_("quantity"),)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """
        Calculate the total cost of the item.

        Returns:
            Decimal: The total cost of the item.
        """
        return self.price * self.quantity
