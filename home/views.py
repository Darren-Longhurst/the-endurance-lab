
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404, HttpResponseNotAllowed
from django.core.exceptions import PermissionDenied
from django.views import View
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

# Contact Section

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Basic Validation check
        if not name or not email or not message:
            messages.error(request, 'Please fill in all fields before submitting.')
            return redirect('contact')

        # Send Email Logic
        send_mail(
            f'Contact Form Inquiry from {name}',
            message,
            email,
            ['theendurancelabmp4@gmail.com'],
        )

        messages.success(request, 'Message sent! We will get back to you soon.')
        return redirect('contact')

    return render(request, 'home/contact.html')

# Privacy Policy

def privacy_policy(request):
    return render(request, "privacy_policy.html")

# --- ERROR TESTING VIEWS ---
# These views are specifically for testing documentation

class Force403View(View):
    def get(self, request, *args, **kwargs):
        raise PermissionDenied

class Force404View(View):
    def get(self, request, *args, **kwargs):
        raise Http404("Page not found test")

class Force405View(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

class Force500View(View):
    def get(self, request, *args, **kwargs):
        raise Exception("Internal server error test")

# --- CUSTOM ERROR HANDLERS ---

def handler403(request, exception):
    """ Custom 403 Forbidden page """
    return render(request, '403.html', status=403)

def handler404(request, exception):
    """ Custom 404 Not Found page """
    return render(request, '404.html', status=404)

def handler405(request, exception=None):
    """ Custom 405 Method Not Allowed page """
    return render(request, '405.html', status=405)

def handler500(request):
    """ Custom 500 Internal Server Error page """
    return render(request, '500.html', status=500)
