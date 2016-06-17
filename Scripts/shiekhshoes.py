#!/usr/bin/env python3
import requests
import re
import timeit
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as bs
from userinfo import *

#User input
useEarlyLink = True
earlyLink = ''
useKeyword = False
#TODO: Make the logic for keyword checkout

#Functions
def checkout(): #USA checkout
    response = session.get('https://www.shiekhshoes.com/checkout.aspx?pType=cc') #TODO: Get rid of this by making a list of state codes
    soup = bs(response.text, 'html.parser')

    stateIds = soup.find_all('option')
    stateId = ''
    for state in stateIds:
        if state.getText() == shipping_state:
            stateId = state['value']
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
        'ShippingFirstName': firstName,
        'ShippingLastName': lastName,
        'ShippingAddress1': shippingAddress1,
        'ShippingAddress2': shippingAddress2,
        'ShippingAptSuite': shippingAptSuite,
        'ShippingZip': shippingZip,
        'ShippingCity': shippingCity,
        'ShippingStateId': stateId,
        'ShippingMethodId': '1',
        'BillingAddressSameAsSippingAddress': 'true',
        'BillingFirstName': firstName,
        'BillingLastName': lastName,
        'BillingCardType': cardType,
        'BillingCardNumber': cardNumber,
        'BillingCardExpirationMonth': cardExpMonth,
        'BillingCardExpirationYear': cardExpYear,
        'BillingCardSecurityCode': cardCvv,
        'OrderNote': '',
        'PhoneNumber': phoneNumber,
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

if useEarlyLink:
    response = session.get(earlyLink)
    soup = bs(response.text, 'html.parser')
    
    sizeCodes = soup.find_all('a', {'class' : 'selectSize'})
    sizeCode = ''
    for code in sizeCodes:
        if code['data-size'] == size:
            sizeCode = code['data-stock']
            continue
        
    payload = {
        '' : sizeCode + ',0'
    }

    response = session.post('http://www.shiekhshoes.com/api/ShoppingCart/AddToCart', data=payload)
    checkout()

stop = timeit.default_timer()
print(stop - start) # Get the runtime
