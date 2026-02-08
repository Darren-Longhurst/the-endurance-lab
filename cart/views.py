from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product, ProductVariant


def view_cart(request):
    """ A view to render the shopping cart page. """
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ Add a quantity of the specific product/variant to the cart """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    variant_id = request.POST.get('product_variant')
    cart = request.session.get('cart', {})

    item_key = f"{item_id}_{variant_id}" if variant_id else str(item_id)

    # Logic to identify what to name in the success message
    display_name = product.name
    if variant_id:
        variant = get_object_or_404(ProductVariant, pk=variant_id)
        display_name = f"{product.name} ({variant.variant_value})"

    if item_key in cart:
        cart[item_key] += quantity
        messages.success(request, f'Updated {display_name} quantity to {cart[item_key]}')
    else:
        cart[item_key] = quantity
        messages.success(request, f'Added {display_name} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """ Adjust the quantity of the specified product key """
    # Note: item_id here will now be the 'item_key' (e.g., "1_5")
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request, f'Updated quantity in your cart')
    else:
        cart.pop(item_id)
        messages.success(request, 'Removed item from your cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """ Remove the item from the cart """
    try:
        cart = request.session.get('cart', {})
        cart.pop(item_id)
        messages.success(request, 'Removed item from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing your item: {e}')
        return HttpResponse(content=e, status=500)
