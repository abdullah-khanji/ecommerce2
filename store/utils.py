import json
from .models import *


def cookieCart(request):

    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    name = []
    pricePro = []
    image = []
    quantity = []
    data_name = []

    for i in cart:
        # We use try block to prevent items in cart that may have been removed from causing error
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])


# below is new vars for cookies
            name = cart[i]['productName']
            proId = cart[i]['productId']
            pricePro = cart[i]['productPrice']
            priceFlo = float(pricePro)
            image = cart[i]['productImage']
            quantity = cart[i]['quantity']
            totalPrice = (float(quantity) * float(priceFlo))
# the above is how to grab the name/quantity/price/imageurl
            data_name.append({
                'name': name,
                'proId': proId,
                'pricePro': pricePro,
                'image': image,
                'quantity': quantity,
                'totalPrice': totalPrice,
                'website': "Meijer",
            })
            order['get_cart_total'] += totalPrice
            order['get_cart_items'] += cart[i]['quantity']
# the above is how to send data to cart/checkout

            item = {
                'id': product.id,
                'product': {'id': product.id, 'name': product.name, 'price': product.price,
                            'imageURL': product.imageURL}, 'quantity': cart[i]['quantity'],
                'digital': product.digital, 'get_total': total,
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items, 'data_name': data_name, 'name': name, 'pricePro': pricePro, 'image': image, 'quantity': quantity}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        cookieData = cookieCart(request)

        data_name = cookieData['data_name']
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        name = cookieData['name']
        pricePro = cookieData['pricePro']
        image = cookieData['image']
        quantity = cookieData['quantity']
        data_name = cookieData['data_name']
        return {'cartItems': cartItems, 'order': order, 'data_name': data_name, 'items': items, 'name': name, 'pricePro': pricePro, 'image': image, 'quantity': quantity}

    return {'cartItems': cartItems, 'order': order, 'items': items, 'data_name': data_name}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']
    total = float(data['form']['total'])

    cookieData = cookieCart(request)
    data_name = cookieData['data_name']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
        totalPrice=total,
        delivered=False,
    )

    for name in data_name:
        #product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=name['name'],
            order=order,
            price=name['pricePro'],
            quantity=name['quantity'],
            store=name['website'],
        )
    return customer, order
