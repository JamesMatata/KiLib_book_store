from django.conf import settings
from django.db import models

from store.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    product = models.ForeignKey(Product, related_name='order_product', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    county = models.CharField(max_length=100)
    deliveryPoint = models.CharField(max_length=150)
    deliveryPoint2 = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.IntegerField()
    price = models.IntegerField(default=1)
    quantity = models.PositiveIntegerField(default=1)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)
    email = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)