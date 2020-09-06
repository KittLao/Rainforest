import json
import datetime
from .models import *

def cookieCart(request):
    # If user isn't authenticated, the cart will be updated without
    # updating the db.
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_total']
    # Prevents the error when programmer manually deleted cookie from 
    # webpage.
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    # Amount of items present in checkout is stored inside the cookie.
    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            # Update total and amount of items in the cart.
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            # Manually build the format of the product without the db.
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)
            if product.digits == False:
                order['shipping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    # Customer can only view their cart if they are logged in.
    if request.user.is_authenticated:
        # Can access customer form user due to one to one relationship.
        customer = request.user.customer
        # If the cart for a customer exists, get it. If not, create it.
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # All items attatched to the order.
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']   

    return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
    # Still want to store the guest user's info on the db.
    # A user will be created automatically. If the same
    # guest user wants to shop but without an account, it
    # would not create a new user.
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    # If the same guest wants to shop but without an account, the
    # email field will ensure a new user would not be created.
    customer, created = Customer.objects.get_or_create(email=email)
    # If the guest user decides to create an account, we can transfer
    # the stored information to the created user.
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(product=product, 
                            order=order, 
                            quantity=item['quantity'])
    return customer, order