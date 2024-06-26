from django.db import models
from django.utils import timezone

class Customer (models.Model):
    User_Name = models.CharField(primary_key = True, max_length = 12)
    Phone_No = models.CharField(max_length = 12)
    Email = models.EmailField()
    Password = models.CharField(max_length = 8)
    Address = models.TextField()

class Product (models.Model):
    Product_Name = models.CharField(max_length = 20, primary_key = True)
    Product_Desc = models.TextField()
    Category = models.CharField(max_length = 15)
    Price = models.FloatField()
    Stock = models.IntegerField()
        
class Order (models.Model):
    Order_ID = models.AutoField(primary_key = True)
    Product_Name = models.ForeignKey(Product, on_delete=models.CASCADE)
    User_Name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Total_Price = models.FloatField()
    Order_Date = models.DateField(default=timezone.now)
    Shipping_Address = models.TextField()

class Review (models.Model):
    Product_Name = models.ForeignKey(Product, on_delete=models.CASCADE)
    Order_ID = models.ForeignKey(Order, on_delete=models.CASCADE)
    Description = models.TextField()
    Rate = models.IntegerField()