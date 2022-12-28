import json
import requests
from django.shortcuts import (
	render,
	redirect,
	get_object_or_404,
)
from django.urls import reverse
from django.http import HttpResponse
from decouple import config
from orders.models import Order
from orders.tasks import order_created




# MERCHANT = config("MERCHANT")
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST_URL = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY_URL = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY_URL = "https://sandbox.zarinpal.com/pg/StartPay/{authority}"
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional


def send_request(request):
	amount = request.session.get("amount")
	currency = "IRT"
	CallbackURL = request.build_absolute_uri(reverse('payments:verify'))
	description = f"پرداخت هزینه سفارشی به مبلغ {amount}"

	request_data = {
		"merchant_id": MERCHANT,
		"amount": amount, # int
		"currency": currency, # Rial -> IRR & Toman -> IRT not required
		"description": description, # required
		"callback_url": CallbackURL, # required
		"metadata": {
			"mobile": "", # optional
			"email": "", # optional
		}
	}
	request_header = {
		"accept": "application/json",
        "content-type": "application/json"
	}

	# send the request to ZP_API_REQUEST
	response = requests.post(ZP_API_REQUEST_URL, 
							 data=json.dumps(request_data), 
							 headers=request_header)
	authority = response.json()['data']['authority']
	code = response.json()['data']['code']
	errors = response.json()['errors']

	request.session["authority"] = authority

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
					   "error_message": error_message,})

def verify(request):
	amount = request.session.get("amount")
	currency = "IRT"
	order_id = request.session.get("order_id")
	send_authority = request.session.get("authority")

	if request.method == 'GET':
		t_status = request.GET.get('Status', None)
		get_authority = request.GET.get('Authority', None)

		if send_authority != get_authority:
			error_message = "مقدار authority ارسالی با مقدار authority دریافتی برابر نیست."
			return render(request,
						  "payments/errors.html",
						  {"error_code": "Authority",
					   	   "error_message": error_message,})


		request_data = {
			"merchant_id": MERCHANT,
			"amount": amount, # int
			"currency": currency, # Rial -> IRR & Toman -> IRT not required
			"authority": get_authority, # required
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
			code = response.json()['data']['code']
			transaction_id = response.json()['data']['ref_id']
			errors = response.json()['errors']

			# check it to sure, transaction successfully
			if len(errors) == 0:
				if code == 100:
					# show successfully transaction and paid order in database
					order = get_object_or_404(Order, id=order_id)
					order.transaction_id = transaction_id
					order.save()

					# launch Asynchronous task
					# order_created.delay(order.id)

					return render(request,
						  		  "payments/payment-success.html",
						         {"order": order})
					
				elif code == 101:
					# show transaction submitted
					order = get_object_or_404(Order, id=order_id)
					return render(request,
						          "payments/payment-success.html",
						         {"order": order})
				else:
					# show failed transaction
					error_code = code
					error_message = "تراکنش شما با خطا مواجه شده است."
					return render(request,
								"payments/payment-unsuccessful-verify.html",
								{"error_code": error_code,
								"error_message": error_message,})

			else:
				# transaction unsuccessful, show failed transaction
				error_code = errors['code']
				error_message = errors['message']
				return render(request,
							  "payments/payment-unsuccessful-verify.html",
							 {"error_code": error_code,
							  "error_message": error_message,})

		elif t_status == 'NOK':
			# Transaction rejected or unsuccuessfully
			# show unsuccessful transaction and unpaid order in database
			# show error message to the user
			return render(request,
						  "payments/payment-unsuccessfull.html",)
	else:
		# method not found
		return HttpResponse('Method not allowed')