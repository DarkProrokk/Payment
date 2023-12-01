from .views import buy_item, item_view, success_view, cancel_view, buy_order, index
from django.urls import path

urlpatterns = [
    path('buy/<int:pk>/', buy_item, name='buy_item'),
    path('item/<int:pk>/', item_view, name='item_view'),
    path('success/', success_view, name='success'),
    path('cansel/', cancel_view, name='cancel'),
    path('order_buy/<int:pk>/', buy_order, name='order_buy'),
    path('', index),
]