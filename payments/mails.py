from django.core.mail import send_mail
from django.conf import settings
from orders.models import Order


def send_mail_payment_successfull(order_id):
    """
    send an e-mail notification when a payment of
    order is successful.
    """
    order = Order.objects.get(id=order_id)

    # mail config
    subject = f"Order nr. {order.id}"
    message = f"Dear {order.full_name},\n\n" \
              f"Your payment has been successfully completed. " \
              f"Your order ID is {order.id}."
    mail_sent = send_mail(subject,
                          message,
                          settings.DEFAULT_FROM_EMAIL,
                          [order.email])

    return mail_sent


def send_mail_payment_unsuccessfull(order_id):
    """
    send an e-mail notification when a payment of
    order is unsuccessful.
    """
    order = Order.objects.get(id=order_id)

    # mail config
    subject = f"Order nr. {order.id}"
    message = f"Dear {order.full_name},\n\n" \
              f"Your payment was unsuccessful. " \
              f"Your order ID is {order.id}."
    mail_sent = send_mail(subject,
                          message,
                          settings.DEFAULT_FROM_EMAIL,
                          [order.email])

    return mail_sent


def send_mail_payment_gateway_inactive(order_id):
    """
    send an e-mail notification when payment gateway
    is inactive.
    """
    order = Order.objects.get(id=order_id)

    # mail config
    subject = f"Order nr. {order.id}"
    message = f"Dear {order.full_name},\n\n" \
              f"Your payment was not processed because the gateway is" \
              f" inactive. " \
              f"Your order ID is {order.id}."
    mail_sent = send_mail(subject,
                          message,
                          settings.DEFAULT_FROM_EMAIL,
                          [order.email])

    return mail_sent
