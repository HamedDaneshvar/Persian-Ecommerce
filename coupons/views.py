from django.shortcuts import (
    redirect,
)
from django.utils import timezone
from coupons.models import Coupon
from coupons.forms import CouponApplyForm


def coupon_apply(request):
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
        del request.session["coupon_code"]

    return redirect("cart:cart_detail")
