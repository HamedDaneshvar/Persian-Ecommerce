from decimal import Decimal
from django.urls import reverse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from transportation.models import Transport
from transportation.forms import TransportChoiceForm
from django.contrib.auth import get_user_model
from orders.models import OrderItem, Order
from orders.forms import OrderCreateForm
# from orders.tasks import order_created
from orders.mails import send_mail_order_created

User = get_user_model()


def order_create(request):
    """
    View function to create a new order.

    This view handles the creation of a new order and the associated order
    items. It validates the order form and the transportation form, saves the
    order, creates the order items, and performs additional tasks such as
    clearing the cart, launching asynchronous tasks, and sending order
    creation emails.

    Parameters:
        - request: The HTTP request object.

    Returns:
        - If the order total cost is zero, it renders the payment success
          template.
        - If the order total cost is non-zero, it redirects to the payment
          request view.
    """
    if request.user.is_anonymous:
        url = reverse('accounts:login') + \
            "?next=" + reverse("orders:order_create")
        return redirect(url)

    user = User.objects.get(id=request.user.id)
    transports = Transport.objects.filter(activate=True)

    cart = Cart(request)

    if request.method == "POST":
        order_form = OrderCreateForm(request.POST, prefix="order_form")
        transportation_form = TransportChoiceForm(request.POST,
                                                  prefix="transportation_form")

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

            if Decimal(order.get_total_cost()) == 0:
                order.paid = True
                return render(request,
                              "payments/payment-success.html",
                              {"code": 100,
                               "order": order})

            request.session['amount'] = order.get_total_cost()
            request.session['order_id'] = order.id

            send_mail_order_created(order.id)
            return redirect('payments:request')

        else:
            return render(request,
                          "orders/order/checkout.html",
                          {"order_form": order_form,
                           "transportation_form": transportation_form,
                           "transports": transports, })
    else:
        order_form = OrderCreateForm(auto_id=False,
                                     instance=user, prefix="order_form")
        transportation_form = TransportChoiceForm(prefix="transportation_form")

        return render(request,
                      "orders/order/checkout.html",
                      {"order_form": order_form,
                       "transportation_form": transportation_form,
                       "transports": transports, })


@login_required
def orders_list(request):
    user = User.objects.get(id=request.user.id)
    orders = Order.objects.filter(email=user.email).order_by("-create_at")
    return render(request,
                  "orders/order/my-orders.html",
                  {'orders': orders})
