from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, ProductVariant


def cart_contents(request):

    cart_items = []
    subtotal = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for item_key, quantity in cart.items():
        if "_" in str(item_key):
            product_id, variant_id = item_key.split('_')
            product = get_object_or_404(Product, pk=product_id)
            variant = get_object_or_404(ProductVariant, pk=variant_id)
            current_price = product.price + variant.price_modifier
        else:
            product = get_object_or_404(Product, pk=item_key)
            variant = None
            current_price = product.price

        lineitem_total = quantity * current_price
        subtotal += lineitem_total
        product_count += quantity

        cart_items.append({
            'item_id': item_key,
            'quantity': quantity,
            'product': product,
            'variant': variant,
            'current_price': current_price,
            'lineitem_total': lineitem_total,
        })

    if subtotal < settings.FREE_DELIVERY_THRESHOLD:
        delivery = subtotal * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - subtotal
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + subtotal

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
