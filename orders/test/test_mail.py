from django.core import mail
from django.test import TestCase
from django.conf import settings
from unittest.mock import patch
from orders.models import Order
from orders.mails import send_mail_order_created


class MailTests(TestCase):
    @patch('orders.models.Order.objects.get')
    def test_send_mail_order_created(self, mock_get_order):
        # Mock the Order object
        order_id = 1
        order_mock = Order(id=order_id,
                           full_name='John Doe',
                           email='test@example.com')
        mock_get_order.return_value = order_mock

        # Call the function
        mail_sent = send_mail_order_created(order_id)

        # Assert that the email was sent
        self.assertEqual(mail_sent, 1)

        # Verify the sent email
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.subject, f"Order nr. {order_id}")
        self.assertEqual(sent_email.body,
                         f"Dear {order_mock.full_name},\n\n"
                         f"You have successfully placed an order."
                         f"Your order ID is {order_id}.")
        self.assertEqual(sent_email.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(sent_email.to, [order_mock.email])

        # Verify that the Order object was retrieved with the correct ID
        mock_get_order.assert_called_once_with(id=order_id)
