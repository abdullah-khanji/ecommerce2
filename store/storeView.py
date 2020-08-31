# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
import requests
import sys
from bs4 import BeautifulSoup, element
from selenium import webdriver, common
from time import sleep
import json
import re


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    data_name = data['data_name']
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    """
	name = data['name']
	pricePro = data['pricePro']
	image = data['image']
	quantity = data['quantity']	
	"""
    # this above is grabbing the data from cartData
    # this is the code for the cart
    """
	data_name.append({
	'name':name,
	'pricePro':pricePro,
	'image':image,
	'quantity':quantity	
	})
	"""
    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'data_name': data_name}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    data_name = data['data_name']
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'data_name': data_name}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    print(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    # error because you customer is not request.user field
    # try this one customer=request.user
    # if it does't work then you must have to remove Customer from the models
    # and instead of customer field in order put user ok you understand.
    # this will solve this issue. you are best.
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        phoneNum=data['shipping']['phone'],
    )

    return JsonResponse('Payment submitted..', safe=False)


def bot_search(request):
    query = request.GET.get('query')

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    i = 0
    data_name = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:79.0) Gecko/20100101 Firefox/79.0'}
    url = f'https://www.meijer.com/shop/en/search/?text={query}'
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print('Connection Error')  # In case the connection fails

    else:
        soup = BeautifulSoup(response.text, "html.parser")
        product_container_list = soup.find_all(
            'div', class_='product-tile-container', limit=5)
        if not product_container_list:
            print('Nothing found!')
        else:
            for product in product_container_list:
                try:
                    name = product.find('a', class_='h7').get_text(strip=True)
                except AttributeError:
                    print('Nothing found!')
                    break
                try:
                    #price = '$' + product.find('span', {'itemprop': 'price'}).get_text(strip=True)
                    price = product.find(
                        'span', {'itemprop': 'price'}).get_text(strip=True)
                except AttributeError:
                    price_sale = product.find(
                        'div', class_='display-price sale-price')
                    price = "".join([t for t in price_sale.contents if type(
                        t) == element.NavigableString]).strip()

                # In case the image is not parsed correctly just ignore it (it's useless anyway)
                image_link = product.find('img')['src'] if product.find('img')[
                    'src'].startswith('https') else ''
                print(f'{name}\n{price}\n{image_link}\n')
                i += 1
                data_name.append({
                    'name': name,
                    'price': price,
                    'image': image_link,
                    'id': i,
                    'website': "Meijer"
                })

    return render(request, 'store/store.html', {'data_name': data_name, 'query': query, 'cartItems': cartItems})
