# work
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from django.shortcuts import render
import re
from time import sleep
from selenium import webdriver, common
from bs4 import BeautifulSoup, element
import sys
import requests
from store.utils import cookieCart, cartData, guestOrder
from store.models import *
import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ViewSet
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from django.utils import timezone
# my imports
from store import models
from .serializers import ProductSerializer, OrderSerializer
# Create your views here.


class ProductListApi(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]


class ProductDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]


class OrderAPI(generics.CreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        a = Order.objects.filter(customer=self.request.user)
        print(a)
        serializer.save(customer=self.request.user)
    # def perform_create(self, serializer):
    #     serializer.save(customer=self.request.user, email='a@gmail.com',
    #                     date_ordered=timezone.now(), complete=True, transaction_id=datetime.datetime.now().timestamp(),
    #                     totalPrice=200)


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

    return JsonResponse({'data_name': data_name['name'], 'query': query, 'cartItems': cartItems})
