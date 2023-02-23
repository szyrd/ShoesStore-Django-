from django.urls import path
from .views import (
    index,
    ShopView,
    checkout,
    OrderCartView,
    ItemDetailView,
    add_to_cart,
    remove_from_cart,
)

app_name = 'shoes'

urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('checkout/', checkout, name='checkout'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('OrderCartView/', OrderCartView.as_view(), name='OrderCartView'),
    path('product/<slug>', ItemDetailView.as_view(), name='product'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>', remove_from_cart, name='remove_from_cart'),

]
