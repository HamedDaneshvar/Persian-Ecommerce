from django.http import HttpResponseRedirect
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth import (
    login,
    authenticate,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from accounts.forms import (
    CustomUserCreationForm,
    ProfileForm,
)
from shop.models import Product
from cart.forms import CartAddProductForm


User = get_user_model()


def signup(request):
    """
    View function for user registration/signup.
    """

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            full_name = form.cleaned_data.get("full_name")
            raw_password = form.cleaned_data.get("password1")
            form = form.save(commit=False)
            form.username = email
            form.nick_name = full_name
            form.save()
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect("shop:product_list")
    else:
        form = CustomUserCreationForm()
    return render(request,
                  "accounts/signup.html",
                  {"form": form, })


@login_required
def profile(request):
    """
    View function to display user profile page.
    """

    return render(request,
                  "accounts/profile.html",)


@login_required
def edit_profile(request):
    """
    View function for editing user profile page.
    """

    user = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if "email" in form.changed_data:
                form.username = form.cleaned_data.get("email")
            form.save()
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=user)

    return render(request,
                  "accounts/edit_profile.html",
                  {"form": form, })


@login_required
def add_remove_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
    else:
        product.users_wishlist.add(request.user)
    try:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    except KeyError:
        return redirect('/')


@login_required
def user_wishlist(request):
    user = request.user
    grid = False
    product_exist = True
    products_description = ""

    # show in grid or list type
    if request.GET.get('style', None) == 'list':
        grid = False
    else:
        grid = True

    products = user.user_wishlist.filter(available=True,)

    if len(products) == 0:
        product_exist = False
        products_description = "شما محصولی را به لیست علاقمندی‌های خود \
                اضافه نکرده‌اید!"

    cart_product_form = CartAddProductForm(auto_id=False,
                                           initial={"override": True, })

    return render(
        request=request,
        template_name='accounts/wishlist.html',
        context={
            'products': products,
            'grid': grid,
            'product_exist': product_exist,
            'products_description': products_description,
            'cart_product_form': cart_product_form,
        }
    )
