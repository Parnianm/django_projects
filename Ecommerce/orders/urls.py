from django.urls import path
from . import views

app_name = 'orders'

# urlpatterns = [
#     path('payments/', views.PaymentListView.as_view(), name='payment_list'),
#     path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),

#     path('orders/', views.OrderListView.as_view(), name='order_list'),
#     path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),

#     path('orders/<int:order_id>/products/', views.OrderProductListView.as_view(), name='order_products'),
#     path('orders/<int:order_id>/products/<int:pk>/', views.OrderProductDetailView.as_view(), name='order_product_detail'),
# ]


urlpatterns = [
    path('payments/', views.payments, name='payments'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_complete/', views.order_complete, name='order_complete'),
]