from cart.cart import Cart


def cart(request):
    """
    Context processor that adds the cart object to the request context.

    This context processor retrieves the cart for the current user from the
    session and adds it to the request context, making it accessible in
    templates as 'cart'. The cart object provides convenient methods to manage
    the products in the cart.
    """
    return {'cart': Cart(request)}
