from django.db import models
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel
from shop.models import Product

class Order(GeneralModel):
	full_name = models.CharField(max_length=128,
								 verbose_name=_("Full name"))
	email = models.EmailField(verbose_name=_("E-mail"))
	phone = models.CharField(max_length=11,
							 verbose_name=_("Phone"),)
	address = models.CharField(max_length=512,
							   verbose_name=_("Address"))
	paid = models.BooleanField(default=False,
							   verbose_name=_("Paid"))

	class Meta:
		ordering = ["-create_at"]
		indexes = [
			models.Index(fields=["-create_at"]),
		]

	def __str__(self):
		return f"Order {self.id}"

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.item.all())


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