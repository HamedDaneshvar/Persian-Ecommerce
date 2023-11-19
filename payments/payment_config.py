from decouple import config


def get_zarinpal_payment_url():
    debug = config("DEBUG", default=False, cast=bool)
    if debug:
        # API URL from banktest.ir for zarinpal gateway
        ZP_API_REQUEST_URL = "https://sandbox.banktest.ir/zarinpal/" \
            + "api.zarinpal.com/pg/v4/payment/request.json"
        ZP_API_VERIFY_URL = "https://sandbox.banktest.ir/zarinpal/" \
            + "api.zarinpal.com/pg/v4/payment/verify.json"
        ZP_API_STARTPAY_URL = "https://sandbox.banktest.ir/zarinpal/" \
            + "www.zarinpal.com/pg/StartPay/{authority}"
    else:
        ZP_API_REQUEST_URL = "https://sandbox.zarinpal.com/pg/v4/payment" \
            + "/request.json"
        ZP_API_VERIFY_URL = "https://sandbox.zarinpal.com/pg/v4/payment" \
            + "/verify.json"
        ZP_API_STARTPAY_URL = "https://sandbox.zarinpal.com/pg/StartPay" \
            + "/{authority}"

    return (ZP_API_REQUEST_URL, ZP_API_VERIFY_URL, ZP_API_STARTPAY_URL)
