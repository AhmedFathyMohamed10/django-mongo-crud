from decimal import Decimal
from bson.decimal128 import Decimal128, create_decimal128_context
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    stock = models.SmallIntegerField(default=1)

    def __str__(self) -> str:
        return self.name
    
class Order(models.Model):
    product_id = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'Order for: {self.user.username} -> {self.product_id.name}'
    
    def save(self, *args, **kwargs):
        self.total_cost = self.get_total_cost()
        super().save(*args, **kwargs)

    def get_total_cost(self):
        if not self.quantity or not self.product_id:
            return 0
        
        try:
            # Convert the product price to a string and then to a Decimal
            price = Decimal(str(self.product_id.price))
            # Ensure that the quantity is also a Decimal
            quantity = Decimal(self.quantity)
            # Calculate the total cost
            total_cost = price * quantity
            return total_cost
        except Exception as e:
            # Handle any exceptions and return None or an appropriate default value
            return None
    
