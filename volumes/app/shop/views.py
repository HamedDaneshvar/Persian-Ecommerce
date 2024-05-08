from datetime import timedelta
from django.utils import timezone
from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.db.models import Avg, Count
from cart.forms import CartAddProductForm
from reviews.forms import ReviewForm
from orders.models import OrderItem
from shop.models import (
    Category,
    Product,
)
from website.models import Slider


def index(request):
    slides = Slider.objects.filter(status=True)
    categories = Category.objects.all()
    highest_rate_product = Product.objects.annotate(avg_rate=Avg(
        'reviews__rate')).order_by('-avg_rate')
    if len(highest_rate_product) > 6:
        highest_rate_product = highest_rate_product[:6]

    today = timezone.now().date()
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=7)

    best_sellers = OrderItem.objects.filter(order__create_at__range=(
        start_date, end_date)).values('product') \
        .annotate(total_sales=Count('product')) \
        .order_by('-total_sales')

    if len(best_sellers) > 4:
        best_sellers = best_sellers[:4]

    product_ids = [item['product'] for item in best_sellers]
    best_sellers = Product.objects.filter(id__in=product_ids) \
        .annotate(avg_rate=Avg('reviews__rate'),
                  rate_count=Count('reviews__rate'))

    featured_products = Product.objects.annotate(num_users=Count(
        'users_wishlist')).order_by('-num_users')

    if len(featured_products) > 4:
        featured_products = featured_products[:4]

    wishlist_products = []
    if request.user.is_authenticated:
        user = request.user
        wishlist_products = user.user_wishlist.filter(available=True)\
            .values_list('id', flat=True)

    return render(request,
                  "shop/index.html",
                  {"slides": slides,
                   "categories": categories,
                   "highest_rate_product": highest_rate_product,
                   "best_sellers_product": best_sellers,
                   "featured_products": featured_products,
                   "wishlist_products": wishlist_products, })


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
    products = Product.objects.filter(available=True,) \
        .annotate(avg_rate=Avg('reviews__rate'),
                  rate_count=Count('reviews__rate'))

    # search query
    if search_q := request.GET.get("q"):
        products = products.filter(name__icontains=search_q)

    wishlist_products = []
    if request.user.is_authenticated:
        user = request.user
        wishlist_products = user.user_wishlist.filter(available=True)\
            .values_list('id', flat=True)

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
            'wishlist_products': wishlist_products,
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
    product_images = product.images.all()

    wishlist_product = []
    if request.user.is_authenticated:
        user = request.user
        wishlist_product = user.user_wishlist.filter(available=True, id=id)

    reviews = product.reviews.filter(status='A')
    try:
        reviews_avg = f"{(sum(reviews.values_list('rate', flat=True)) / len(reviews)):.1f}"
    except ZeroDivisionError:
        reviews_avg = 0

    filled_stars = int(float(reviews_avg))
    unfilled_stars = 5 - filled_stars

    cart_product_form = CartAddProductForm()
    review_form = ReviewForm(auto_id=False,)

    return render(
        request=request,
        template_name='shop/product/detail.html',
        context={
            'product': product,
            'product_images': product_images,
            'cart_product_form': cart_product_form,
            'review_form': review_form,
            'wishlist_product': wishlist_product,
            'reviews': reviews,
            'reviews_avg': reviews_avg,
            'filled_stars': range(filled_stars),
            'unfilled_stars': range(unfilled_stars),
        }
    )
