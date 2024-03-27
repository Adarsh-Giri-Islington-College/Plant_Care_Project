from django.db import models
from users.models import User
from products.models import Product


class Cart(models.Model):
    cart_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart {self.cart_id}"
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def sub_total(self):
        return self.product.product_price * self.quantity

    def __str__(self):
        return f"{self.product}" 
