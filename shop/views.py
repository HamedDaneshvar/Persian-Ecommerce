from django.shortcuts import (
	render,
	get_object_or_404,
)
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
	
	return render(
		request=request,
		template_name='shop/product/list.html',
		context={
			'category': category,
			'categories': categories,
			'products': products,
			'grid': grid,
		}
	)

def product_detail(request, id, slug):
	product = get_object_or_404(
		Product,
		id=id,
		slug=slug,
		available=True,
	)

	return render(
		request=request,
		template_name='shop/product/detail.html',
		context={
			'product': product,
		}
	)