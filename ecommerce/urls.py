from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),

    # Cart
    path('cart/', views.cart_list, name='cart_list'),
    path('cart/<int:pk>/', views.cart_detail, name='cart_detail'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/<int:pk>/delete/', views.cart_item_delete, name='cart_item_delete'),
]
