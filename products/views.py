from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Product, Category, ProductVariant
from .forms import ProductForm

# Create your views here.

def all_products(request):
    """Show all products, including sorting, category filtering, special offers and search."""

    products = Product.objects.all()
    all_categories = Category.objects.all()

    # Defaults
    query = ""
    categories = None
    special_offers = False
    sort = None
    direction = None

    # --- Sorting ---
    sort = request.GET.get("sort")
    direction = request.GET.get("direction")

    if sort:
        sortkey = sort
        if sort == "name":
            products = products.annotate(lower_name=Lower("name"))
            sortkey = "lower_name"
        elif sort == "category":
            sortkey = "category__name"

        if direction == "desc":
            sortkey = f"-{sortkey}"

        products = products.order_by(sortkey)

    # --- Category filtering ---
    category_param = request.GET.get("category")
    if category_param:
        category_names = category_param.split(",")
        products = products.filter(category__name__in=category_names)
        categories = Category.objects.filter(name__in=category_names)

    # --- Special offers ---
    if request.GET.get("special_offers"):
        special_offers = True
        products = products.filter(is_special_offer=True)

    # --- Search ---
    if "q" in request.GET:
        query = request.GET.get("q", "").strip()
        if not query:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('products'))
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
        "all_categories": all_categories,
        "special_offers": special_offers,
        "current_sorting": f"{sort}_{direction}",
    }
    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

@login_required
def add_product(request):
    """ Add a product to the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store with confirmation """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    # Show confirmation page first
    if request.method == "GET":
        return render(request, 'products/delete_product.html', {
            'product': product
        })

    # Confirmed delete (POST)
    if request.method == "POST":
        product.delete()
        messages.success(request, 'Product deleted!')
        return redirect(reverse('products'))


def top_rated_products(request):
    """ A view to show the highest rated products """
    products = Product.objects.filter(rating__isnull=False).order_by('-rating')
    context = {
        'products': products,
        'title': 'Top Rated',
    }
    return render(request, 'products/products.html', context)
