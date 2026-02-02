
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import ContactInquiry
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
