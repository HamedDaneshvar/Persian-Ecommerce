from django.shortcuts import (
    render,
    get_object_or_404,
)
from cart.forms import CartAddProductForm
from shop.models import (
    Category,
    Product,
)


def product_list(request, category_slug=None):
    """
    View function for displaying a list of products.

    Args:
        request: The HTTP request object.
        category_slug: Optional category slug to filter products by category.

    Returns:
        The rendered template with the list of products.
    """

    category = None
    grid = False
    product_exist = True
    products_description = ""
    categories = Category.objects.all()
    products = Product.objects.filter(available=True,)
    if len(products) == 0:
        product_exist = False
        products_description = "این فروشگاه محصولی را ثبت نکرده است."

    if category_slug and product_exist:
        category = get_object_or_404(
            Category,
            slug=category_slug,
        )
        products = products.filter(category=category)
        if len(products) == 0:
            product_exist = False
            products_description = "برای این دسته‌بندی محصولی ثبت نشده است."

    # show in grid or list type
    if request.GET.get('style', None) == 'list':
        grid = False
    else:
        grid = True

    cart_product_form = CartAddProductForm(auto_id=False,
                                           initial={"override": True, })

    return render(
        request=request,
        template_name='shop/product/list.html',
        context={
            'category': category,
            'categories': categories,
            'products': products,
            'product_exist': product_exist,
            'products_description': products_description,
            'grid': grid,
            'cart_product_form': cart_product_form,
        }
    )


def product_detail(request, id, slug):
    """
    View function for displaying the details of a product.

    Args:
        request: The HTTP request object.
        id: The ID of the product.
        slug: The slug of the product.

    Returns:
        The rendered template with the product details.
    """

    product = get_object_or_404(
        Product,
        id=id,
        slug=slug,
        available=True,
    )

    cart_product_form = CartAddProductForm()

    return render(
        request=request,
        template_name='shop/product/detail.html',
        context={
            'product': product,
            'cart_product_form': cart_product_form,
        }
    )
