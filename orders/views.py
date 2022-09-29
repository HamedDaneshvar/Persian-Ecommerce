from django.shortcuts import (
	render,
	get_object_or_404,
)
from cart.cart import Cart
from transportation.models import Transport
from transportation.forms import TransportChoiceForm
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created

def order_create(request):
	cart = Cart(request)

	if request.method == "POST":
		order_form = OrderCreateForm(request.POST, prefix="order_form")
		transportation_form = TransportChoiceForm(request.POST, prefix="transportation_form")

		if order_form.is_valid() and transportation_form.is_valid():
			order = order_form.save(commit=False)
			transport = transportation_form.cleaned_data["transport"]
			order.transport = get_object_or_404(Transport, id=transport.id)

			if cart.coupon:
				order.coupon = cart.coupon
				order.discount = cart.coupon.discount
			order.save()
			for item in cart:
				OrderItem.objects.create(order=order,
										 product=item["product"],
										 price=item["price"],
										 quantity=item["quantity"],)
			
			# clear the cart
			cart.clear()
			
			# launch Asynchronous task
			# order_created.delay(order.id)
			
			return render(request,
						  "orders/order/payment-success.html",
						  {"order": order})
		else:
			return render(request,
					  "orders/order/checkout.html",
					  {"order_form": order_form,})
	else:
		order_form = OrderCreateForm(auto_id=False, prefix="order_form")
		transportation_form = TransportChoiceForm(prefix="transportation_form")

		transports = Transport.objects.filter(activate=True)

		return render(request,
					  "orders/order/checkout.html",
					  {"order_form": order_form,
					   "transportation_form": transportation_form,
					   "transports": transports,})