from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# the models for products.
class Product(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    price = models.TextField()
    product_logo = models.TextField()

    def __str__(self):
        return self.name


# the basket models, used to link a user with the products they added to their basket.
class Basket(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.TextField()