from django.db import models
from users.models import User
from django.utils import timezone
from products.models import Product


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Khalti', 'Khalti'),
        ('Cash on Delivery', 'Cash on Delivery'),
    ]

    payment_id = models.BigAutoField(primary_key=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment {self.payment_id}"
    

class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
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