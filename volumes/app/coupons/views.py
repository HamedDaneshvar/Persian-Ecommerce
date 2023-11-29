from django.shortcuts import (
    redirect,
)
from django.utils import timezone
from coupons.models import Coupon
from coupons.forms import CouponApplyForm


def coupon_apply(request):
    """
    Apply a coupon code.

    This view function handles the process of applying a coupon code in the
    e-commerce system. It receives a POST request with the coupon code,
    validates it, and updates the session with the coupon information. If the
    coupon is valid, the session will store the coupon ID and code; otherwise,
    the session will store None for the coupon ID.
    Finally, the function redirects the user to the cart detail page.

    Args:
        request (HttpRequest): The HTTP request object containing the coupon
        code.

    Returns:
        HttpResponseRedirect: A redirect response to the cart detail page.

    """
    now = timezone.now()
    if request.method == "POST":
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            try:
                coupon = Coupon.objects.get(code__iexact=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True,)
                request.session["coupon_id"] = coupon.id
                request.session["coupon_code"] = code
            except Coupon.DoesNotExist:
                request.session["coupon_id"] = None
                request.session["coupon_code"] = code
        else:
            request.session["coupon_id"] = None
    else:
        request.session["coupon_id"] = None
        try:
            del request.session["coupon_code"]
        except KeyError:
            pass

    return redirect("cart:cart_detail")
