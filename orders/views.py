from django.shortcuts import render
from cart.cart import Cart
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created

def order_create(request):
	cart = Cart(request)

	if request.method == "POST":
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save(commit=False)
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
			order_created.delay(order.id)
			
			return render(request,
						  "orders/order/payment-success.html",
						  {"order": order})
		else:
			return render(request,
					  "orders/order/checkout.html",
					  {"form": form,})
	else:
		form = OrderCreateForm(auto_id=False)
		return render(request,
					  "orders/order/checkout.html",
					  {"form": form,})