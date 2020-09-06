from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    # User can only have only customer and customer 
    # can only have one user.
    user = models.OneToOneField(User, 
                    null=True, 
                    blank=True, 
                    on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    # If the product is digital, it does not need to be shipped.
    digital = models.BooleanField(default=False, null=True, blank=True)
    # Needs image field.
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except :
            url = ''
        return url

class Order(models.Model):
    # Every customer has an order. If a customer gets deleted,
    # do not want to delete the order, just set the customer
    # value to null.
    customer = models.ForeignKey(Customer, 
                    on_delete=models.SET_NULL, 
                    null=True, 
                    blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    # If false then user hasn't made the order yet. Can still
    # add stuff to it.
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        # If any of the items are not digital, then the order
        # needs to be shipped.
        for order in orderitems:
            if order.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
 
# Unique items in the cart.
class OrderItem(models.Model):
    product = models.ForeignKey(Product, 
                    on_delete=models.SET_NULL, 
                    null=True)
    # An item in a cart can have multiple orders of product of
    # the same product.
    order = models.ForeignKey(Order, 
                    on_delete=models.SET_NULL, 
                    null=True)
    # Amount of duplicate products.
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    # Shipping address should be attatched to a customer 
    # because if an order gets deleted, there still needs
    # to be a shipping address for a customer.
    customer = models.ForeignKey(Customer, 
                    on_delete=models.SET_NULL, 
                    null=True)
    # Order for shipping address.
    order = models.ForeignKey(Order, 
                    on_delete=models.SET_NULL, 
                    null=True)
    # Base fields for shipping address.
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

