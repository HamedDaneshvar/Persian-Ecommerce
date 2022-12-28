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
					validators=[MinValueValidator(0),
								MaxValueValidator(100),])
	transaction_id = models.IntegerField(verbose_name=_("Transaction ID"), 
										 null=True)

	class Meta:
		ordering = ["-create_at"]
		indexes = [
			models.Index(fields=["-create_at"]),
		]

	def __str__(self):
		return f"Order {self.id}"

	def get_total_cost_before_discount(self):
		return sum(item.get_cost() for item in self.items.all())

	def get_discount(self):
		total_cost = self.get_total_cost_before_discount()
		if self.discount:
			return total_cost * (self.discount / Decimal(100))
		return Decimal(0)

	def get_total_cost(self):
		transport_price = Decimal(0)
		if self.transport:
			transport_price = self.transport.price
		total_cost = self.get_total_cost_before_discount() + transport_price
		return total_cost - self.get_discount()
	get_total_cost.short_description = _("Total cost")

	def transport_name(self):
		return self.transport.name
	transport_name.short_description = "Transport Type"


class OrderItem(GeneralModel):
	order = models.ForeignKey(Order,
							  on_delete=models.CASCADE,
							  related_name="items",)
	product = models.ForeignKey(Product,
								on_delete=models.CASCADE,
								related_name="order_items",)
	price = models.DecimalField(max_digits=10,
								decimal_places=2,
								verbose_name=_("Price"))
	quantity = models.PositiveIntegerField(default=1,
										   verbose_name=_("quantity"),)

	def __str__(self):
		return str(self.id)

	def get_cost(self):
		return self.price * self.quantity