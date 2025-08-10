from django.contrib import admin
from .models import Payment, Order, OrderProduct

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'payment_method', 'amount_paid', 'status', 'created_at')
    search_fields = ('payment_id', 'user__username', 'payment_method', 'status')
    list_filter = ('status', 'payment_method', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'is_ordered', 'created_at', 'updated_at')
    search_fields = ('order_number', 'user__username', 'first_name', 'last_name', 'email', 'phone')
    list_filter = ('status', 'is_ordered', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'user', 'quantity', 'product_price', 'ordered', 'created_at')
    search_fields = ('product__product_name', 'order__order_number', 'user__username')
    list_filter = ('ordered', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
