from django.shortcuts import render
from products.models import Product

# Create your views here.

def index(request):
    """
    A simple view to render the home page.
    """
    latest_products = Product.objects.order_by('-id')[:3]

    context = {
        'latest_products': latest_products,
    }
    return render(request, 'home/index.html', context)
