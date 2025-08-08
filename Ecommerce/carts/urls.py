from django.urls import path
from . import views


urlpatterns = [
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('decrease/<int:product_id>/', views.decrease_cart, name='decrease_cart'),
    path('', views.cart, name='cart'),

    path('checkout/', views.checkout, name='checkout'),
]