from django.shortcuts import (
	render,
	redirect,
	get_object_or_404,
)
from cart.cart import Cart
from transportation.models import Transport
from transportation.forms import TransportChoiceForm
from django.contrib.auth import get_user_model
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from .mails import send_mail_order_created

User = get_user_model()

def order_create(request):
	user = User.objects.get(id=request.user.id)
	transports = Transport.objects.filter(activate=True)
	
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

			request.session['amount'] = order.get_total_cost()
			request.session['order_id'] = order.id
			# return redirect('payments:request')

			send_mail_order_created(order.id)
			return render(request,
						  "orders/order/payment-success.html",
						  {"order": order})
		else:
			return render(request,
					  "orders/order/checkout.html",
					  {"order_form": order_form,
					   "transportation_form": transportation_form,
					   "transports": transports,})
	else:
		order_form = OrderCreateForm(auto_id=False, instance=user, prefix="order_form")
		transportation_form = TransportChoiceForm(prefix="transportation_form")

		return render(request,
					  "orders/order/checkout.html",
					  {"order_form": order_form,
					   "transportation_form": transportation_form,
					   "transports": transports,})