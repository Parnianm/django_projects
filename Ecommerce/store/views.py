from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product
from carts.models import Cart, CartItem
from category.models import Category
from carts.views import _cart_id
from django.db.models import Q 


def search(request):
    query = request.GET.get('q')
    products = []
    products_count = 0

    if query:
        products = Product.objects.filter(
            Q(product_name__icontains=query) | Q(description__icontains=query),
            is_available=True
        ).order_by('-created_date')
        products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count,
        'search_query': query,
    }

    return render(request, 'store/store.html', context)


def store(request, category_slug=None):
    """
    نمایش صفحه فروشگاه با امکان فیلتر بر اساس دسته‌بندی و صفحه‌بندی.
    """

    products = Product.objects.select_related('category').filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category).order_by('-id')

    paginator = Paginator(products, 6)
    page = request.GET.get('page')

    try:
        paged_products = paginator.page(page)
    except PageNotAnInteger:
        paged_products = paginator.page(1)
    except EmptyPage:
        paged_products = paginator.page(paginator.num_pages)

    context = {
        'products': paged_products,
        'products_count': products.count(),
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    """
    نمایش جزئیات یک محصول خاص، و بررسی اینکه آیا در سبد خرید کاربر هست یا نه.
    """

    product = get_object_or_404(
        Product.objects.select_related('category'),
        slug=product_slug,
        category__slug=category_slug
    )

    cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
    product_in_cart = False

    if cart:
        product_in_cart = CartItem.objects.filter(
            cart=cart, product=product
        ).exists()

    context = {
        'product': product,
        'product_in_cart': product_in_cart,
    }

    return render(request, 'store/product_detail.html', context)
