import re
import json
from decimal import Decimal
import requests
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.urls import reverse
from django.http import HttpResponse
from payments.models import Payment
from payments.payment_config import get_zarinpal_payment_url
from payments.mails import (
    send_mail_payment_successfull,
    send_mail_payment_unsuccessfull,
    send_mail_payment_gateway_inactive,
)
from orders.models import Order

# CONSTANT
CURRENCY = "IRT"


def get_merchant():
    payments = Payment.objects.filter(available=True)
    if not payments:
        return False

    # get zarinpal merchant from db
    global ZARINPAL_MERCHANT
    ZARINPAL_MERCHANT = payments.filter(types="zarinpal")\
        .values_list("merchant")[0][0]

    return True


def get_payments_url():
    # get zarinpal payment urls
    zarinpal_urls = get_zarinpal_payment_url()
    global ZP_API_REQUEST_URL
    global ZP_API_VERIFY_URL
    global ZP_API_STARTPAY_URL
    ZP_API_REQUEST_URL = zarinpal_urls[0]
    ZP_API_VERIFY_URL = zarinpal_urls[1]
    ZP_API_STARTPAY_URL = zarinpal_urls[2]


def send_request(request):
    gateway_status = get_merchant()
    if not gateway_status:
        print("We have receive your order but gateway is not active!")
        # return to template when gateway is not active
        return redirect("payments:inactive_gateway")

    get_zarinpal_payment_url()

    amount = request.session.get("amount")
    callbackURL = request.build_absolute_uri(reverse('payments:verify'))
    description = f"پرداخت هزینه سفارشی به مبلغ {amount}"

    # change type of amount if possiable to int
    pattern = r'(\d+)\.0+'
    amount_temp = re.match(pattern, amount)
    if amount_temp:
        amount = int(amount_temp.group(1))

        # cause banktest or zarinpal bug to send amount as toman
        amount *= 10

        request.session['amount'] = amount

    request_data = {
        "merchant_id": ZARINPAL_MERCHANT,
        "amount": amount,  # int
        "currency": CURRENCY,  # Rial -> IRR & Toman -> IRT not required
        "description": description,  # required
        "callback_url": callbackURL,  # required
        "metadata": {
            "mobile": "",  # optional
            "email": "",  # optional
        }
    }
    request_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    #
    if not isinstance(amount, int):
        error_code = "local 1"
        error_message = "مبلغ ارسالی به درگاه باید از نوع int باشد."
        return render(request,
                      "payments/errors.html",
                      {"error_code": error_code,
                       "error_message": error_message, })

    # send the request to ZP_API_REQUEST
    response = requests.post(ZP_API_REQUEST_URL,
                             data=json.dumps(request_data),
                             headers=request_header)
    try:
        authority = response.json()['data']['authority']
        code = response.json()['data']['code']
        errors = response.json()['errors']
        request.session["authority"] = authority
    except:
        errors = response.json()['errors']
        code = None

    # success operations
    if code == 100 and len(errors) == 0:
        # send user to the zarinpal gateway and doing Transaction
        # after that zarinpal will return user to callback_url
        return redirect(ZP_API_STARTPAY_URL.format(authority=authority))
    else:
        error_code = errors['code']
        error_message = errors['message']
        return render(request,
                      "payments/errors.html",
                      {"error_code": error_code,
                       "error_message": error_message, })


def verify(request):
    amount = request.session.get("amount")
    order_id = request.session.get("order_id")
    send_authority = request.session.get("authority")

    if request.method == 'GET':
        t_status = request.GET.get('Status', None)
        get_authority = request.GET.get('Authority', None)

        if send_authority != get_authority:
            error_message = \
                "مقدار authority ارسالی با مقدار authority دریافتی برابر نیست."
            return render(request,
                          "payments/errors.html",
                          {"error_code": "Authority",
                           "error_message": error_message, })

        request_data = {
            "merchant_id": ZARINPAL_MERCHANT,
            "amount": amount,  # int
            "currency": CURRENCY,  # Rial -> IRR & Toman -> IRT not required
            "authority": get_authority,  # required
        }
        request_header = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        if t_status == 'OK':
            # Transaction successfully completed
            response = requests.post(ZP_API_VERIFY_URL,
                                     data=json.dumps(request_data),
                                     headers=request_header)
            try:
                code = response.json()['data']['code']
                transaction_id = response.json()['data']['ref_id']
                fee = response.json()['data']['fee']

                # cause banktest or zarinpal bug to get amount as toman
                fee /= 10

                errors = response.json()['errors']
            except:
                send_mail_payment_unsuccessfull(order_id)
                errors = response.json()['errors']
                error_code = errors['code']
                error_message = errors['message']
                return render(request,
                              "payments/payment-unsuccessful-verify.html",
                              {"error_code": error_code,
                               "error_message": error_message, })

            # check it to sure, transaction successfully
            if len(errors) == 0:
                if code == 100:
                    # show successfully transaction and paid order in database
                    order = get_object_or_404(Order, id=order_id)
                    order.transaction_id = transaction_id
                    order.paid = True
                    order.fee = Decimal(fee)
                    order.save()

                    # launch Asynchronous task
                    # order_created.delay(order.id)
                    send_mail_payment_successfull(order_id)
                    return render(request,
                                  "payments/payment-success.html",
                                  {"code": code,
                                   "order": order})

                elif code == 101:
                    # show transaction submitted
                    order = get_object_or_404(Order, id=order_id)
                    return render(request,
                                  "payments/payment-success.html",
                                  {"code": code,
                                   "order": order})
                else:
                    # show failed transaction
                    send_mail_payment_unsuccessfull(order_id)
                    error_code = code
                    error_message = "تراکنش شما با خطا مواجه شده است."
                    return render(request,
                                  "payments/payment-unsuccessful-verify.html",
                                  {"error_code": error_code,
                                   "error_message": error_message, })

            else:
                # transaction unsuccessful, show failed transaction
                send_mail_payment_unsuccessfull(order_id)
                error_code = errors['code']
                error_message = errors['message']
                return render(request,
                              "payments/payment-unsuccessful-verify.html",
                              {"error_code": error_code,
                               "error_message": error_message, })

        elif t_status == 'NOK':
            # Transaction rejected or unsuccuessfully
            # show unsuccessful transaction and unpaid order in database
            # show error message to the user
            send_mail_payment_unsuccessfull(order_id)
            return render(request,
                          "payments/payment-unsuccessful.html",)
        else:
            send_mail_payment_unsuccessfull(order_id)
            error_code = "local verify 1"
            error_message = "تایید تراکنش شما با خطا مواجه شده است."
            return render(request,
                          "payments/payment-unsuccessful-verify.html",
                          {"error_code": error_code,
                           "error_message": error_message, })
    else:
        # method not found
        return HttpResponse('Method not allowed')


def inactive_gateway(request):
    order_id = request.session.get("order_id", None)
    send_mail_payment_gateway_inactive(order_id)
    return render(request,
                  "payments/payment-gateway-inactive.html",
                  {"order_id": order_id})
