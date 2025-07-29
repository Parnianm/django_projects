from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product,Variation
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# def add_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     product_variations = []
#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#     except Cart.DoesNotExist:
#         cart = Cart.objects.create(cart_id=_cart_id(request))
#         cart.save()

#     try:
#         cart_item = CartItem.objects.get(product=product, cart=cart)
#         cart_item.quantity += 1
#         cart_item.save()
#     except CartItem.DoesNotExist:
#         cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#         cart_item.save()

#     return redirect('cart')  

def _get_variations_from_request(product, request):
    """استخراج variationهای معتبر از درخواست"""
    variations = []
    for key, value in request.POST.items():
        try:
            variation = Variation.objects.get(
                product=product,
                category__name__iexact=key,
                value__iexact=value
            )
            variations.append(variation)
        except Variation.DoesNotExist:
            continue
    return variations

def _get_or_create_cart(request):
    """برگرداندن سبد خرید مرتبط با session"""
    cart_id = _cart_id(request)
    cart, created = Cart.objects.get_or_create(cart_id=cart_id)
    return cart

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variations = _get_variations_from_request(product, request)
    cart = _get_or_create_cart(request)

    cart_items = CartItem.objects.filter(product=product, cart=cart)
    for item in cart_items:
        existing_variations = list(item.variations.all())
        if existing_variations == product_variations:
            item.quantity += 1
            item.save()
            break
    else:
        # اگر آیتم با همین variation وجود نداشت، یکی بساز
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        if product_variations:
            cart_item.variations.set(product_variations)
        cart_item.save()

    return redirect('cart')


def decrease_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    product_variations = []
    for key in request.GET:
        value = request.GET.get(key)
        try:
            variation = Variation.objects.get(
                product=product,
                category__name__iexact=key,
                value__iexact=value
            )
            product_variations.append(variation)
        except Variation.DoesNotExist:
            pass

    cart_items = CartItem.objects.filter(product=product, cart=cart)

    for item in cart_items:
        existing_variations_set = set(item.variations.values_list('id', flat=True))
        new_variations_set = set(variation.id for variation in product_variations)

        if existing_variations_set == new_variations_set:
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
            break

    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    product_variations = []
    for key in request.GET:
        value = request.GET.get(key)
        try:
            variation = Variation.objects.get(
                product=product,
                category__name__iexact=key,
                value__iexact=value
            )
            product_variations.append(variation)
        except Variation.DoesNotExist:
            pass

    cart_items = CartItem.objects.filter(product=product, cart=cart)

    for item in cart_items:
        existing_variations_set = set(item.variations.values_list('id', flat=True))
        new_variations_set = set(variation.id for variation in product_variations)

        if existing_variations_set == new_variations_set:
            item.delete()
            break

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        # tax = 0 
        # grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        cart_items = []

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)
