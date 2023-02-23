from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .models import Item, OrderItem, Order


def checkout(request):
    return render(request, 'checkout.html')


def index(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'index.html', context)


def product(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'product-single.html', context)


class ShopView(ListView):
    model = Item
    template_name = "shop.html"


def shop(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'shop.html', context)


class OrderCartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "cart.html", context)
        except ObjectDoesNotExist:
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-single.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Need Check Order item in Order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        return redirect("shoes:product", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Need Check Order item in Order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
        else:
            return redirect("shoes:product", slug=slug)
    else:
        return redirect("shoes:product", slug=slug)

    return redirect("shoes:product", slug=slug)
