from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.http import Http404
from django.views.decorators.http import require_POST
from shop.models import Product
from coupons.forms import CouponApplyForm
from cart.cart import Cart
from cart.forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart.

    This view function handles the POST request to add a product to the cart.
    It retrieves the product based on the provided product ID, validates the
    form data submitted by the user, and adds the product to the cart with the
    specified quantity. After adding the product, the user is redirected to
    the cart detail page.

    Args:
        request: The HTTP request object.
        product_id: The ID of the product to be added to the cart.

    Returns:
        Redirects to the cart detail page.

    Raises:
        Http404: If the product with the specified ID does not exist.
    """
    cart = Cart(request)
    try:
        product = get_object_or_404(Product, id=product_id)
    except Http404:
        return render(request, "cart/detail.html", status=404)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd["quantity"],
                 override_quantity=cd["override"])
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    """
    Remove a product from the cart.

    This view function handles the POST request to remove a product from the
    cart. It retrieves the product based on the provided product ID and
    removes it from the cart. After removing the product, the user is
    redirected to the cart detail page.

    Args:
        request: The HTTP request object.
        product_id: The ID of the product to be removed from the cart.

    Returns:
        Redirects to the cart detail page.

    Raises:
        Http404: If the product with the specified ID does not exist.
    """
    cart = Cart(request)
    try:
        product = get_object_or_404(Product, id=product_id)
    except Http404:
        return render(request, "cart/detail.html", status=404)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    Display the cart detail page.

    This view function renders the cart detail page, which shows the products
    currently in the cart. It retrieves the cart object from the request, adds
    the update quantity form for each item in the cart, and includes the
    coupon apply form. The rendered page includes the cart information and
    forms for updating quantities and applying coupons.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered cart detail page.
    """
    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(initial={
            "quantity": item["quantity"],
            "override": True, },
            auto_id=False,)

    coupon_apply_form = CouponApplyForm()

    return render(request,
                  "cart/detail.html",
                  {"cart": cart,
                   "coupon_apply_form": coupon_apply_form})
