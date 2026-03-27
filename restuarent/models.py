from django.db import models
from django.contrib.auth.models import User
import random
import string



class Entry(models.Model):
    CATEGORY_CHOICES = [
        ('popular', 'Popular Dish'),
        ('main', 'Main Course'),
        ('beverage', 'Beverage'),
    ]
    product_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.URLField(max_length=300)
    size = models.CharField(max_length=50)
    flavour = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='popular')



class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=20)  
    email = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address_line = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    landmark = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.full_name

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Entry, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"{self.product.name} - {self.order.order_id}"   
    

class admin(models.Model):   
    admin_id = models.AutoField(primary_key=True)
    admin_email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    