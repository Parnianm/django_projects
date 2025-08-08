from .models import Cart, CartItem
from .views import _cart_id
from django.db.models import Sum

def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # for item in cart_items:
        #     item_count += item.quantity

        # نسخه بهینه شده 
        item_count = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0      

    except Cart.DoesNotExist:
        item_count = 0

    return dict(cart_items_count=item_count)
