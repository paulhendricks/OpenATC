#!/usr/bin/env python3
import requests
import re
import timeit
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as bs
from userinfo import *

#User input
use_early_link = True
early_link = ''
use_keyword = False
#TODO: Make the logic for keyword checkout

#Functions
def checkout(): #USA checkout
    response = session.get('https://www.shiekhshoes.com/checkout.aspx?pType=cc') #TODO: Get rid of this by making a list of state codes
    soup = bs(response.text, 'html.parser')

    state_ids = soup.find_all('option')
    state_id = ''
    for state in state_ids:
        if state.getText() == shipping_state:
            state_id = state['value']
            continue

    payload = {
        'Key' : '1',
        'Value' : 'UPS ($0.00)'
    }
    
    response = session.post('https://www.shiekhshoes.com/api/ShoppingCart/UpdateShippingMethod', data=payload)

    payload = {
        '__VIEWSTATEGENERATOR': '277BF4AB',
        'blackbox': '',
        'ShippingCountryId': '222', #USA code
        'ShippingFirstName': first_name,
        'ShippingLastName': last_name,
        'ShippingAddress1': shipping_address_1,
        'ShippingAddress2': shipping_address_2,
        'ShippingAptSuite': shipping_apt_suite,
        'ShippingZip': shipping_zip,
        'ShippingCity': shipping_city,
        'ShippingStateId': state_id,
        'ShippingMethodId': '1',
        'BillingAddressSameAsSippingAddress': 'true',
        'BillingFirstName': first_name,
        'BillingLastName': last_name,
        'BillingCardType': card_type,
        'BillingCardNumber': card_number,
        'BillingCardExpirationMonth': card_exp_month,
        'BillingCardExpirationYear': card_exp_year,
        'BillingCardSecurityCode': card_cvv,
        'OrderNote': '',
        'PhoneNumber': phone_number,
        'GuestEmail': email,
        'CacheStatus': 'cached',
        'HasShippingAddress': 'false',
        'PayWithPayPal': 'false',
        'CustomerEmailAddress': '',
        'CustomerFirstName': '',
        'CustomerLastName': ''
    }

    response = session.post('https://www.shiekhshoes.com/api/ShoppingCart/ProcessCheckout', data=payload)
    print (response.text)
    
#Main
start = timeit.default_timer()

session = requests.session()

if use_early_link:
    response = session.get(early_link)
    soup = bs(response.text, 'html.parser')
    
    size_codes = soup.find_all('a', {'class' : 'selectSize'})
    size_code = ''
    for code in size_codes:
        if code['data-size'] == size:
            size_code = code['data-stock']
            continue
        
    payload = {
        '' : size_code + ',0'
    }

    response = session.post('http://www.shiekhshoes.com/api/ShoppingCart/AddToCart', data=payload)
    checkout()

stop = timeit.default_timer()
print(stop - start) # Get the runtime
