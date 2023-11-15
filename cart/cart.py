from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart():
    """
    Represents a shopping cart for a user session.
    """

    def __init__(self, request):
        """
        Initializes the cart for every session (user).
        If the cart exists, it sets the cart; otherwise, it creates a new one.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Store current applied coupon
        self.coupon_id = self.session.get("coupon_id")

    def add(self, product, quantity=1, override_quantity=False):
        """
        Adds a product to the cart or updates its quantity.

        Parameters:
        - product: The product to be added or updated.
        - quantity: The quantity of the product to be added.
        - override_quantity: A boolean indicating whether to override the
          existing quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0,
                                     "price": str(product.price), }
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        """
        Marks the session as "modified" to ensure it gets saved.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Removes a product from the cart.

        Parameter:
        - product: The product to be removed from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

        # Remove coupon from session if cart is empty
        if len(self) == 0:
            try:
                if self.session.get("coupon_id", None):
                    del self.session["coupon_id"]
                    del self.session["coupon_code"]
            except:
                pass

    def __iter__(self):
        """
        Iterates over the items in the cart and gets the corresponding
        products from the database.
        """
        product_ids = self.cart.keys()
        # Get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Returns the total number of items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """
        Returns the total price of all items in the cart.
        """
        return sum(Decimal(item["price"]) * item["quantity"]
                   for item in self.cart.values())

    def clear(self):
        """
        Remove cart and coupon from session
        """
        del self.session[settings.CART_SESSION_ID]
        self.cart = {}
        if self.session.get("coupon_id", None):
            del self.session["coupon_id"]
            del self.session["coupon_code"]
        self.save()

    @property
    def coupon(self):
        """
        Returns the applied coupon if exists; otherwise, returns None.
        """
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """
        Returns the discount amount based on the applied coupon.
        """
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) \
                    * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """
        Returns the total price after applying the discount.
        """
        return self.get_total_price() - self.get_discount()
