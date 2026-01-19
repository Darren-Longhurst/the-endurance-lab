from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Product, Category, ProductVariant

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    special_offers = False

    if request.GET:
        # Handle category filtering
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
        # Special offers filtering
        if 'special_offers' in request.GET:
            special_offers = True
            products = products.filter(is_special_offer=True)
        # Handle search queries
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return render(request, 'products/products.html', {'products': products})

            queries = (
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query if 'q' in request.GET else '',
        'current_categories': categories,
        'special_offers': special_offers,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
