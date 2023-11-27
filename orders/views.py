from decimal import Decimal
from django.http import Http404
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
            order.user = user
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
    """
    View function to display a list of orders for the logged-in user.

    This view retrieves all orders associated with the currently logged-in user
    and displays them in descending order based on their creation date. If no
    orders are found, the user is redirected to the orders list page.

    Parameters:
        - request: The HTTP request object.

    Returns:
        - Renders the 'orders/order/my-orders.html' template, passing the
          retrieved orders as the 'orders' context variable.
    """
    user = request.user
    orders = user.orders.all().order_by("-create_at")
    return render(request,
                  "orders/order/my-orders.html",
                  {'orders': orders})


@login_required
def order_detail(request, id):
    """
    View function to display the details of a specific order.

    This view retrieves the order associated with the currently logged-in user
    and the provided order ID. If the order is not found, the user is
    redirected to the orders list page. Otherwise, the order details and the
    associated items are rendered in the 'orders/order/detail.html' template.

    Parameters:
        - request: The HTTP request object.
        - id: The ID of the order to display.

    Returns:
        - Renders the 'orders/order/detail.html' template, passing the
          retrieved order as the 'order' context variable and its associated
          items as the 'items' context variable.
    """
    user = request.user
    try:
        order = get_object_or_404(Order, user=user, id=id)
        items = order.items.all()
    except Http404:
        return render(request, "404.html", status=404)

    return render(request,
                  "orders/order/detail.html",
                  {"order": order,
                   "items": items})


@login_required
def send_to_payment(request, order_id):
    """
    View function to redirect the user to the payment request page.

    This view retrieves the order associated with the currently logged-in user
    and the provided order ID. If the order is not found, the user is
    redirected to the orders list page. Otherwise, the order's total cost is
    stored in the session along with the order ID. The user is then redirected
    to the payment request view.

    Parameters:
        - request: The HTTP request object.
        - order_id: The ID of the order to send to payment.

    Returns:
        - Redirects the user to the payment request view.

    Raises:
        - Http404: If the order with the provided ID is not found.
    """
    user = request.user
    try:
        order = get_object_or_404(Order, user=user, id=order_id)
    except Http404:
        return render(request, "404.html", status=404)
    amount = order.get_total_cost()
    request.session["amount"] = amount
    request.session["order_id"] = order_id
    return redirect("payments:request")
