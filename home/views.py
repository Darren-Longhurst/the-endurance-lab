
from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from .forms import NewsletterForm

def index(request):
    """ A view to return the index page, top rated products, and newsletter signup """

    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, 'Successfully subscribed to the Lab!')
            return redirect('home')
        else:
            messages.error(request, 'Failed to subscribe. Please ensure the email is valid.')
    else:
        newsletter_form = NewsletterForm()

    top_rated = Product.objects.filter(rating__isnull=False).order_by('-rating', '-id')[:3]

    context = {
        'top_rated_products': top_rated,
        'newsletter_form': newsletter_form,
    }

    return render(request, 'home/index.html', context)
