import timeit
import requests
import re
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as bs

#Constants
base_url = 'http://www.supremenewyork.com'

#Inputs
keywords_category = ['accessories'] # Demo stuff, feel free to change 
keywords_model = ['Mendini', 'Tray', 'Ceramic']
keywords_style = ['Multi']

#Functions
def product_page(url):
    session = requests.session()
    response = session.get(base_url + url)
    soup = bs(response.text, 'html.parser')
        
    h1 = soup.find('h1', {'itemprop' : 'name'})
    p = soup.find('p', {'itemprop' : 'model'})
    if not h1 is None:
        name = h1.getText()
        if not p is None:
            style = p.getText()
            for keyword in keywords_model:
                if keyword in name:
                    for keyword in keywords_style:
                        if keyword in style:
                            print ('FOUND: ' + name + ' AT ' + base_url + url)
                            form = soup.find('form', {'action' : re.compile('(?<=/shop/)(.*)(?=/add)')})
                            if not form is None:
                                payload = {
                                    'utf8' : '✓',
                                    'authenticity_token' : form.find('input', {'name' : 'authenticity_token'})['value'],
                                    'size' : form.find('input', {'name' : 'size'})['value'],
                                    'commit' : 'add to cart'
                                }
                                response1 = session.post(base_url + form['action'], data=payload)
                                print ('Added to cart!')
                                return (session)

def checkout(session):
    print ('Filling out checkout info...')
    response = session.get('https://www.supremenewyork.com/checkout')
    soup = bs(response.text, 'html.parser')
    form = soup.find('form', {'action' : '/checkout'})

    payload = {
        'utf8' : '✓',
        'authenticity_token' : form.find('input', {'name' : 'authenticity_token'})['value'],
        'order[billing_name]' : first_name + ' ' + last_name,
        'order[email]' : email,
        'order[tel]' : phone_number,
        'order[billing_address]' : shipping_address_1,
        'order[billing_address_2]' : shipping_apt_suite,
        'order[billing_zip]' : shipping_zip,
        'order[billing_city]' : shipping_city,
        'order[billing_state]' : shipping_state,
        'order[billing_country]' : shipping_country,
        'same_as_billing_address' : '1',
        'store_credit_id' : '',
        'credit_card[type]' : card_type,
        'credit_card[cnb]' : card_number,
        'credit_card[month]' : card_exp_month,
        'credit_card[year]' : card_exp_year,
        'credit_card[vval]' : card_cvv,
        'order[terms]' : '0',
        'hpcvv' : '',
        'cnt': '2'
    }

    response = session.get('https://www.supremenewyork.com/checkout.js', data=payload)

    payload = {
        'utf8' : '✓',
        'authenticity_token' : form.find('input', {'name' : 'authenticity_token'})['value'],
        'order[billing_name]' : first_name + ' ' + last_name,
        'order[email]' : email,
        'order[tel]' : phone_number,
        'order[billing_address]' : shipping_address_1,
        'order[billing_address_2]' : shipping_apt_suite,
        'order[billing_zip]' : shipping_zip,
        'order[billing_city]' : shipping_city,
        'order[billing_state]' : shipping_state,
        'order[billing_country]' : shipping_country,
        'same_as_billing_address' : '1',
        'store_credit_id' : '',
        'credit_card[type]' : card_type,
        'credit_card[cnb]' : card_number,
        'credit_card[month]' : card_exp_month,
        'credit_card[year]' : card_exp_year,
        'credit_card[vval]' : card_cvv,
        'order[terms]' : '1',
        'hpcvv' : ''
    }

    response = session.post('https://www.supremenewyork.com/checkout', data=payload)
    print (response.text)
    print ('Done! Check confirmation page.')

#Main
start = timeit.default_timer()

session1 = requests.session()
response1 = session1.get('http://www.supremenewyork.com/shop/all')
soup1 = bs(response1.text, 'html.parser')
links1 = soup1.find_all('a', href=True)
links_by_keyword1 = []
for link in links1:
    for keyword in keywords_category:
        if keyword in link['href']:
            links_by_keyword1.append(link['href'])

pool1 = ThreadPool(len(links_by_keyword1))

nosession = True;
while (nosession):
    print ('Finding matching products...')
    result1 = pool1.map(product_page, links_by_keyword1)
    for session in result1:
        if not session is None:
            nosession = False
            checkout(session)
            break

stop = timeit.default_timer()
print(stop - start) # Get the runtime
