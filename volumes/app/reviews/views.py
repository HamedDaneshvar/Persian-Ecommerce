from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from shop.models import Product
from reviews.forms import ReviewForm


# Create your views here.
@login_required
def create_review(request, id):
    user = request.user
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user
            product = get_object_or_404(Product, id=id)
            review.product = product
            review.save()
            messages.info(request, _('دیدگاه شما با موفقیت ثبت شد و پس از\
                                      بررسی نمایش داده خواهد شد.'))
        else:
            messages.error(request, _('ثبت دیدگاه شما با خطا مواجه شد!'))
    return redirect(reverse('shop:product_detail', args=[product.id,
                                                         product.slug]))
