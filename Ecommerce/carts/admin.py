from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'date_added']
    search_fields = ['cart_id']
    list_filter = ['date_added']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'is_active']
    list_filter = ['is_active']
    search_fields = ['product__name', 'cart__cart_id']
