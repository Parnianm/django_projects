from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import datetime
import json

from carts.models import CartItem
from store.models import Product
from .models import Order, Payment, OrderProduct
from .forms import OrderForm


@login_required
@transaction.atomic
def payments(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    order = get_object_or_404(Order, user=request.user, is_ordered=False, order_number=body.get('orderID'))

    payment = Payment.objects.create(
        user=request.user,
        payment_id=body.get('transID', ''),
        payment_method=body.get('payment_method', ''),
        amount_paid=order.order_total,
        status=body.get('status', 'pending'),
    )

    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        order_product = OrderProduct.objects.create(
            order=order,
            payment=payment,
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            product_price=item.product.price,
            ordered=True,
        )
        order_product.variations.set(item.variations.all())
        order_product.save()

        # کم کردن موجودی محصول
        product = item.product
        product.stock -= item.quantity
        product.save()

    # پاک کردن سبد خرید
    cart_items.delete()

    # ارسال ایمیل تایید سفارش
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send(fail_silently=True)  # اگر مشکلی بود ادامه بده

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


@login_required
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = current_user
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # ساخت شماره سفارش
            current_date = datetime.date.today().strftime("%Y%m%d")
            data.order_number = f"{current_date}{data.id}"
            data.save()

            order = get_object_or_404(Order, user=current_user, is_ordered=False, order_number=data.order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


@login_required
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = get_object_or_404(Order, order_number=order_number, is_ordered=True)
        payment = get_object_or_404(Payment, payment_id=transID)
        ordered_products = OrderProduct.objects.filter(order=order)

        subtotal = sum(item.product_price * item.quantity for item in ordered_products)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)

    except Exception:
        return redirect('home')
