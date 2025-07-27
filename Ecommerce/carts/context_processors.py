from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            item_count += item.quantity
    except Cart.DoesNotExist:
        item_count = 0

    return dict(cart_items_count=item_count)
