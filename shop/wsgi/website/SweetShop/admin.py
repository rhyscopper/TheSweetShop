from django.contrib import admin
from SweetShop.models import Product, Basket


# Allows Product and Basket models to be seen in admin through browser.
admin.site.register(Product)
admin.site.register(Basket)