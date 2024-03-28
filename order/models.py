from django.db import models
from users.models import User
from django.utils import timezone
from products.models import Product


class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, through='OrderItem') 

    def __str__(self):
        return f"Order{self.order_id}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def sub_total(self):
        return self.product.product_price * self.quantity

    def __str__(self):
        return f"{self.product}" 