from django.shortcuts import reverse

from django.conf import settings
from django.db import models

CATEGORY_CHOICES = (
    ('WC', 'Winter collection'),
    ('SC', 'Summer collection'),
    ('AS', 'Autumn-spring collection')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    image = models.ImageField(upload_to="shoes_image", blank=True, null=True)
    slug = models.SlugField(default='m')
    description = models.TextField(default='g')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shoes:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("shoes:add_to_cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("shoes:remove_from_cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
