from django.shortcuts import (
	render,
	get_object_or_404,
)
from cart.forms import CartAddProductForm
from .models import (
	Category,
	Product,
)

def product_list(request, category_slug=None):
	category = None
	grid = False
	categories = Category.objects.all()
	products = Product.objects.filter(available=True,)

	if category_slug:
		category = get_object_or_404(
			Category,
			slug=category_slug,
		)
		products = products.filter(category=category)

	# show in grid or list type
	if request.GET.get('stype', None) == 'list':
		grid = False
	else:
		grid = True

	cart_product_form = CartAddProductForm(auto_id=False, 
										   initial={"override": True,})
	
	return render(
		request=request,
		template_name='shop/product/list.html',
		context={
			'category': category,
			'categories': categories,
			'products': products,
			'grid': grid,
			'cart_product_form': cart_product_form,
		}
	)

def product_detail(request, id, slug):
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