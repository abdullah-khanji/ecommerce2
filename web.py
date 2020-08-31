import requests, sys
from bs4 import BeautifulSoup, element
from selenium import webdriver, common
from time import sleep
import json
import re

# product = input('What product are you searching for? ')
def search_walmart(product):
    # Searches the web for the asked product and prints what it finds
    response = []
    res = requests.get(f'https://www.walmart.com/search/?query={product.lower()}' + ''.join(sys.argv[1:]))
    try: 
      res.raise_for_status()
    except requests.exceptions.HTTPError: 
      pass
    except requests.exceptions.ConnectionError: 
      pass
      # print('Connection Error')  # In case the connection fails

    else:
      soup = BeautifulSoup(res.text, "html.parser")
      # print('Walmart.com: \n')
      response = []
      for i in range(5):  # Getting only the first 5 products from the page
        item = {}
        try:
          outcome_grid = soup.find('li', {'data-tl-id': f'ProductTileGridView-{i}'})  # Finds the grid of the item
          outcome_text = outcome_grid.find('div', {'class': 'search-result-product-title gridview'})  # Then it's text\
          brand_or_name = outcome_text.a.span.get_text(' ', strip=True)  # The brand if it exists, otherwise - name
        except AttributeError:
          # print('No such sellable product...\n')
          break
        try:  # Some products don't have a brand and that will raise the error below
          name_after_brand = outcome_text.a.span.next_sibling.get_text(' ', strip=True)
        except AttributeError:
          name_after_brand = None

        try:  # There are some products with no displayed price
          price = outcome_grid.find('span', {'class': 'price-group'}).get_text(strip=True)
        except AttributeError:
          price = 'Price not displayed'
        
        # print(brand_or_name)
        item['name'] = brand_or_name
        if name_after_brand:  # If the brand is displayed
          # print(name_after_brand)
          item['name'] = name_after_brand
        if price:  # If the price is displayed
          # print(price)
          item['price'] = price

        # In case the image is not parsed correctly just ignore it (it's useless anyway)
        image_link = outcome_grid.find('img')['src'] if outcome_grid.find('img')['src'].startswith('https') else ''
        # print(image_link, '\n')  # Prints the image link
        item['image'] = {'url':image_link}
        item['website_link'] = 'Walmart.com'

        response.append(item)

    return response


def search_target(formatted_product):
    '''
    This function uses a different approach. As target.com uses an API to display most of the data on the website,
    BeautifulSoup is useless. So, we can make the request directly to the API and it will give us all the data even faster.
    The data is stored as a json file from which the needed products and their price will be extracted.
    '''

    # This is the url to the API (not the website)
    url = f'''https://redsky.target.com/v2/plp/search/?channel=web&count=96&keyword={formatted_product}
              &offset=0&pricing_store_id=3991&key=ff457966e64d5e877fdbad070f276d18ecec4a01'''

    data = requests.get(url).json()  # Gets the data from the API response

    # print('Target.com: \n')
    response = []
    for i in data['search_response']['items']['Item'][:5]:  # Gets the first 5 products
      item = {
                'name': i['title'], 
                'price':i['price']['formatted_current_price'],
                'image':{'url':i['images'][0]['base_url']+i['images'][0]['primary']},
                'website_link': 'Target.com'
                }
      response.append(item)
      # print('{:<60}\n{}\n{}\n'.format(i['title'], i['price']['formatted_current_price'], 
      #       i['images'][0]['base_url']+i['images'][0]['primary']))
    return response


def search_meijer(formatted_product):
    '''
    Meijer leaves the requests (and the whole program) hanging, so I tricked it by using a Mozilla User Agent
    '''
    # print('Meijer.com:\n')
    data_response = []
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:79.0) Gecko/20100101 Firefox/79.0'}
    url = f'https://www.meijer.com/shop/en/search/?text={formatted_product}'
    response = requests.get(url, headers=headers)
    # print(response)
    try: 
      response.raise_for_status()
    except requests.exceptions.HTTPError: 
      pass
      # print('Connection Error')  # In case the connection fails

    else:
      soup = BeautifulSoup(response.text, "html.parser")
      product_container_list = soup.find_all('div', class_='product-tile-container', limit=5)
      if not product_container_list:
        pass
        # print('Nothing found!')
      else:
        # print(product_container_list)
        for product in product_container_list:
          # print(product)
          item = {}
          try:
            name = product.find('a', class_='h7').get_text(strip=True)
          except AttributeError:
            # print('Nothing found!')
            break
          try:
            price = '$' + product.find('span', {'itemprop': 'price'}).get_text(strip=True)
          except AttributeError:
            price_sale = product.find('div', class_='display-price sale-price')
            price = 'Sale!: ' + "".join([t for t in price_sale.contents if type(t)==element.NavigableString]).strip()

          # In case the image is not parsed correctly just ignore it (it's useless anyway)
          image_link = product.find('img')['src'] if product.find('img')['src'].startswith('https') else ''
          # print(f'{name}\n{price}\n{image_link}\n')
          data_response.append({
                            'name': name, 
                            'price': price, 
                            'image': {'url':image_link},
                            'website_link': 'Meijer.com'
                          })
    return data_response


# The program won't run in Sublime because of the not supported input
product = "comic book"

# print(product)

#product = input('What are you searching for? ')
final_output = []
formatted_product = '+'.join(product.split(' '))  # The website accepts only splitted words by '+'

# We are calling walmart bot first. Storing its output to walmart variable.
walmart = search_walmart(product)

# Extending final_output with walmart's response
final_output.extend(walmart)

# We are calling target bot. Storing its output to target variable.
target = search_target(formatted_product)

# Extending final_output with target's response
final_output.extend(target)

# We are calling meijer bot. Storing its output to meijer variable.
meijer = search_meijer(formatted_product)

# Extending final_output with meijer's response
final_output.extend(meijer)

print(final_output)